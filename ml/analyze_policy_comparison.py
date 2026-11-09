import csv
import json
import math
import os
import statistics
from itertools import combinations

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "experiments",
    "results",
    "dqn_comparison",
    "policy_comparison_episode_metrics.csv",
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "experiments",
    "results",
    "dqn_comparison",
    "statistical_analysis",
)

POLICIES = [
    "Round Robin",
    "Resource Only",
    "Dynamic QoS",
    "DQN",
]

METRICS = {
    "mean_simulated_execution_time": "lower",
    "deadline_success_rate": "higher",
    "mean_qos_score": "higher",
}

REFERENCE_POLICY = "Dynamic QoS"
ZERO_TOLERANCE = 1e-12
TIE_REL_TOLERANCE = 1e-10


def load_episode_data(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Comparison CSV not found: {path}"
        )

    data = {}

    with open(
        path,
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        reader = csv.DictReader(file)

        required = {
            "policy",
            "seed",
            "tasks_completed",
            "all_tasks_completed",
            *METRICS.keys(),
        }

        missing = required - set(reader.fieldnames or [])

        if missing:
            raise ValueError(
                f"CSV is missing required columns: {sorted(missing)}"
            )

        for row in reader:
            policy = row["policy"]
            seed = int(row["seed"])

            if policy not in POLICIES:
                continue

            data.setdefault(policy, {})

            if seed in data[policy]:
                raise ValueError(
                    f"Duplicate row for policy={policy}, seed={seed}"
                )

            if int(row["all_tasks_completed"]) != 1:
                raise ValueError(
                    f"Incomplete episode: policy={policy}, seed={seed}"
                )

            data[policy][seed] = {
                metric: float(row[metric])
                for metric in METRICS
            }

    if not data:
        raise ValueError("No valid episode data was found.")

    reference_seeds = set(data.get(REFERENCE_POLICY, {}))

    for policy in POLICIES:
        if policy not in data:
            raise ValueError(f"Missing policy: {policy}")

        if set(data[policy]) != reference_seeds:
            raise ValueError(
                f"Seed mismatch for {policy}; paired comparison "
                "requires the same seeds for every policy."
            )

    if len(reference_seeds) < 2:
        raise ValueError("At least two matched seeds are required.")

    return data, sorted(reference_seeds)


def average_ranks(values):
    """Return average ranks for tied absolute differences."""
    ordered = sorted(
        range(len(values)),
        key=lambda index: values[index],
    )
    ranks = [0.0] * len(values)
    tie_groups = []
    position = 0

    while position < len(ordered):
        end = position + 1

        while (
            end < len(ordered)
            and math.isclose(
                values[ordered[end]],
                values[ordered[position]],
                rel_tol=TIE_REL_TOLERANCE,
                abs_tol=ZERO_TOLERANCE,
            )
        ):
            end += 1

        # Ranks are one-based; the group occupies
        # ranks position+1 through end.
        average_rank = ((position + 1) + end) / 2.0

        for index in range(position, end):
            ranks[ordered[index]] = average_rank

        tie_groups.append(end - position)
        position = end

    return ranks, tie_groups


def wilcoxon_signed_rank(x, y):
    """
    Two-sided Wilcoxon signed-rank test.

    Uses exact enumeration of sign assignments for up to 25
    non-zero paired differences, with average ranks for ties.
    For larger samples, uses a tie-corrected normal approximation
    with continuity correction.

    The exact sign-enumeration p-value is based on the smaller
    observed rank sum and is invariant to reversing the pairs.
    """
    if len(x) != len(y):
        raise ValueError(
            "Wilcoxon inputs must have the same number of observations."
        )

    differences = [
        float(a) - float(b)
        for a, b in zip(x, y)
    ]

    if not all(math.isfinite(value) for value in differences):
        raise ValueError(
            "Wilcoxon inputs must contain only finite numeric values."
        )

    nonzero = [
        difference
        for difference in differences
        if not math.isclose(
            difference,
            0.0,
            rel_tol=0.0,
            abs_tol=ZERO_TOLERANCE,
        )
    ]

    n = len(nonzero)

    if n == 0:
        return {
            "statistic": 0.0,
            "p_value": 1.0,
            "nonzero_pairs": 0,
            "method": "all paired differences are zero",
        }

    absolute_values = [abs(value) for value in nonzero]
    ranks, tie_groups = average_ranks(absolute_values)

    positive_sum = sum(
        ranks[index]
        for index, value in enumerate(nonzero)
        if value > 0
    )

    negative_sum = sum(
        ranks[index]
        for index, value in enumerate(nonzero)
        if value < 0
    )

    statistic = min(positive_sum, negative_sum)
    total_rank = sum(ranks)

    if n <= 25:
        # Under the signed-rank null distribution, every assignment
        # of signs to the observed absolute ranks is enumerated.
        # Use the smaller observed rank sum to obtain a two-sided
        # p-value that is invariant to swapping x and y.
        observed = min(positive_sum, negative_sum)
        extreme = 0
        total = 1 << n

        for mask in range(total):
            candidate = sum(
                ranks[index]
                for index in range(n)
                if mask & (1 << index)
            )

            if (
                candidate <= observed + ZERO_TOLERANCE
                or candidate >= (
                    total_rank - observed - ZERO_TOLERANCE
                )
            ):
                extreme += 1

        p_value = extreme / total
        method = "exact sign enumeration with tied average ranks"

    else:
        mean_rank_sum = n * (n + 1) / 4.0

        tie_correction = sum(
            size**3 - size
            for size in tie_groups
        )

        variance = (
            n * (n + 1) * (2 * n + 1)
            - tie_correction / 2.0
        ) / 24.0

        if variance <= 0:
            p_value = 1.0
        else:
            # Continuity correction for the normal approximation.
            distance = abs(positive_sum - mean_rank_sum)
            corrected_distance = max(0.0, distance - 0.5)
            z = corrected_distance / math.sqrt(variance)
            p_value = math.erfc(z / math.sqrt(2.0))

        method = (
            "normal approximation with tie correction "
            "and continuity correction"
        )

    return {
        "statistic": statistic,
        "p_value": min(1.0, max(0.0, p_value)),
        "nonzero_pairs": n,
        "method": method,
    }


def holm_adjust(p_values):
    """Holm step-down family-wise error correction."""
    if not all(
        math.isfinite(value) and 0.0 <= value <= 1.0
        for value in p_values
    ):
        raise ValueError("P-values must be finite values in [0, 1].")

    count = len(p_values)
    order = sorted(
        range(count),
        key=lambda index: p_values[index],
    )

    adjusted = [1.0] * count
    running_max = 0.0

    for rank, index in enumerate(order):
        candidate = (count - rank) * p_values[index]
        running_max = max(running_max, candidate)
        adjusted[index] = min(1.0, running_max)

    return adjusted


def describe(values):
    return {
        "n": len(values),
        "mean": statistics.mean(values),
        "population_std": statistics.pstdev(values),
        "median": statistics.median(values),
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data, seeds = load_episode_data(INPUT_FILE)

    summary = {
        "input_file": os.path.relpath(INPUT_FILE, PROJECT_ROOT),
        "matched_seeds": seeds,
        "number_of_paired_episodes": len(seeds),
        "reference_policy": REFERENCE_POLICY,
        "significance_level": 0.05,
        "multiple_testing_correction": (
            "Holm, applied separately to the three comparisons "
            "within each metric"
        ),
        "metrics": {},
        "paired_tests": [],
        "interpretation_notes": [
            "Tests use matched episode-level values for the same seeds.",
            "The reference policy is Dynamic QoS.",
            "Execution time differences are comparison minus reference; negative favors the comparison policy.",
            "Deadline success and QoS differences are comparison minus reference; positive favors the comparison policy.",
            "Zero paired differences are omitted from the signed-rank calculation.",
            "Exact sign enumeration is used for up to 25 non-zero pairs; larger samples use a tie-corrected normal approximation with continuity correction.",
            "These are simulated outcomes, not real-world measurements.",
            "Statistical significance does not by itself establish practical importance or real-world superiority.",
        ],
    }

    test_rows = []

    for metric, preferred_direction in METRICS.items():
        summary["metrics"][metric] = {
            policy: describe([
                data[policy][seed][metric]
                for seed in seeds
            ])
            for policy in POLICIES
        }

        comparisons = [
            policy for policy in POLICIES
            if policy != REFERENCE_POLICY
        ]

        raw_results = []

        for policy in comparisons:
            comparison_values = [
                data[policy][seed][metric]
                for seed in seeds
            ]
            reference_values = [
                data[REFERENCE_POLICY][seed][metric]
                for seed in seeds
            ]

            differences = [
                a - b
                for a, b in zip(
                    comparison_values,
                    reference_values,
                )
            ]

            test = wilcoxon_signed_rank(
                comparison_values,
                reference_values,
            )

            raw_results.append({
                "metric": metric,
                "comparison_policy": policy,
                "reference_policy": REFERENCE_POLICY,
                "comparison_mean": statistics.mean(comparison_values),
                "reference_mean": statistics.mean(reference_values),
                "mean_paired_difference": statistics.mean(differences),
                "median_paired_difference": statistics.median(differences),
                "preferred_direction": preferred_direction,
                **test,
            })

        adjusted = holm_adjust([
            result["p_value"] for result in raw_results
        ])

        for result, adjusted_p in zip(raw_results, adjusted):
            result["holm_adjusted_p_value"] = adjusted_p
            result["significant_after_holm_at_0_05"] = (
                adjusted_p < 0.05
            )

            if preferred_direction == "lower":
                result["direction_favors_comparison_policy"] = (
                    result["mean_paired_difference"] < 0
                )
            else:
                result["direction_favors_comparison_policy"] = (
                    result["mean_paired_difference"] > 0
                )

            summary["paired_tests"].append(result)
            test_rows.append(dict(result))

    json_path = os.path.join(
        OUTPUT_DIR,
        "paired_statistical_summary.json",
    )
    csv_path = os.path.join(
        OUTPUT_DIR,
        "paired_statistical_tests.csv",
    )

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(test_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(test_rows)

    print("\nPaired statistical analysis complete.")
    print("Matched episodes:", len(seeds))
    print("Reference policy:", REFERENCE_POLICY)
    print("Correction: Holm, separately within each metric")
    print("JSON summary:", json_path)
    print("CSV tests:", csv_path)

    print("\nPaired comparisons against Dynamic QoS:")

    for result in summary["paired_tests"]:
        print(
            f"\nMetric: {result['metric']}"
            f"\n  Policy: {result['comparison_policy']}"
            f"\n  Mean paired difference: "
            f"{result['mean_paired_difference']:.6f}"
            f"\n  Wilcoxon p-value: {result['p_value']:.6g}"
            f"\n  Holm-adjusted p-value: "
            f"{result['holm_adjusted_p_value']:.6g}"
            f"\n  Significant after correction: "
            f"{result['significant_after_holm_at_0_05']}"
        )


if __name__ == "__main__":
    main()
