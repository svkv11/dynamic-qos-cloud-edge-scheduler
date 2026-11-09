from ml.analyze_policy_comparison import (
    INPUT_FILE,
    POLICIES,
    REFERENCE_POLICY,
    METRICS,
    average_ranks,
    wilcoxon_signed_rank,
)

import csv


def dp_exact_pvalue(differences):
    """Calculate exact signed-rank p-value using dynamic programming."""

    nonzero = [
        difference
        for difference in differences
        if abs(difference) > 1e-12
    ]

    if not nonzero:
        return 1.0, 0

    ranks, _ = average_ranks(
        [abs(difference) for difference in nonzero]
    )

    # Convert average ranks into integers by multiplying by two.
    scaled_ranks = [
        int(round(2 * rank))
        for rank in ranks
    ]

    total_scaled = sum(scaled_ranks)

    # Count possible signed rank sums.
    counts = [0] * (total_scaled + 1)
    counts[0] = 1

    current_max = 0

    for rank in scaled_ranks:
        for subtotal in range(current_max, -1, -1):
            counts[subtotal + rank] += counts[subtotal]

        current_max += rank

    positive_sum = sum(
        rank
        for rank, difference in zip(ranks, nonzero)
        if difference > 0
    )

    negative_sum = sum(
        rank
        for rank, difference in zip(ranks, nonzero)
        if difference < 0
    )

    observed = min(positive_sum, negative_sum)

    lower = int(round(2 * observed))
    upper = total_scaled - lower

    extreme = sum(
        count
        for rank_sum, count in enumerate(counts)
        if rank_sum <= lower or rank_sum >= upper
    )

    p_value = extreme / (2 ** len(nonzero))

    return p_value, len(nonzero)


def main():
    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    print("\nINDEPENDENT EXACT-P-VALUE VERIFICATION")
    print("=" * 65)

    for metric in METRICS:
        print(f"\nMetric: {metric}")

        for policy in POLICIES:
            if policy == REFERENCE_POLICY:
                continue

            reference_values = {
                row["seed"]: float(row[metric])
                for row in rows
                if row["policy"] == REFERENCE_POLICY
            }

            policy_values = {
                row["seed"]: float(row[metric])
                for row in rows
                if row["policy"] == policy
            }

            common_seeds = sorted(
                set(reference_values) & set(policy_values)
            )

            if not common_seeds:
                print(f"\nPolicy: {policy} — no matching seeds")
                continue

            policy_sample = [
                policy_values[seed]
                for seed in common_seeds
            ]

            reference_sample = [
                reference_values[seed]
                for seed in common_seeds
            ]

            paired_differences = [
                policy_values[seed] - reference_values[seed]
                for seed in common_seeds
            ]

            project_result = wilcoxon_signed_rank(
                policy_sample,
                reference_sample,
            )

            project_p = project_result["p_value"]
            project_n = project_result["nonzero_pairs"]

            if project_n > 25:
                print(
                    f"\nPolicy: {policy}"
                    f"\nExact DP verification skipped "
                    f"(non-zero pairs = {project_n})"
                )
                continue

            dp_p, dp_n = dp_exact_pvalue(paired_differences)

            difference = abs(project_p - dp_p)

            print(f"\nPolicy: {policy}")
            print(f"Non-zero pairs: {dp_n}")
            print(f"Project p-value: {project_p:.12g}")
            print(f"DP exact p-value: {dp_p:.12g}")
            print(f"Absolute difference: {difference:.12g}")

            if difference < 1e-12:
                print("Result: MATCH")
            else:
                print("Result: MISMATCH")


if __name__ == "__main__":
    main()