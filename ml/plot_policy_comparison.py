from pathlib import Path
import csv
import matplotlib.pyplot as plt


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "dqn_comparison"
    / "policy_comparison_episode_metrics.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "dqn_comparison"
    / "figures"
)

POLICY_ORDER = [
    "Round Robin",
    "Resource Only",
    "Dynamic QoS",
    "DQN",
]

POLICY_LABELS = {
    "Round Robin": "Round Robin",
    "Resource Only": "Resource Only",
    "Dynamic QoS": "Dynamic QoS",
    "DQN": "DQN",
}

METRICS = [
    {
        "column": "mean_simulated_execution_time",
        "filename": "mean_simulated_execution_time.png",
        "title": "Mean Simulated Execution Time by Scheduling Policy",
        "ylabel": "Simulated execution time (seconds)",
        "lower_is_better": True,
    },
    {
        "column": "deadline_success_rate",
        "filename": "deadline_success_rate.png",
        "title": "Deadline Success Rate by Scheduling Policy",
        "ylabel": "Deadline success rate (%)",
        "lower_is_better": False,
    },
    {
        "column": "mean_qos_score",
        "filename": "mean_qos_score.png",
        "title": "Mean QoS Score by Scheduling Policy",
        "ylabel": "Mean QoS score",
        "lower_is_better": False,
    },
]


def load_data():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input CSV was not found: {INPUT_FILE}"
        )

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("The comparison CSV contains no rows.")

    results = {}

    for policy in POLICY_ORDER:
        policy_rows = [
            row for row in rows
            if row["policy"] == policy
        ]

        if not policy_rows:
            raise ValueError(
                f"No data found for policy: {policy}"
            )

        if any(
            int(row["tasks_completed"])
            != int(row["expected_tasks"])
            for row in policy_rows
        ):
            raise ValueError(
                f"Incomplete episode found for {policy}."
            )

        results[policy] = policy_rows

    return results


def plot_metric(results, metric):
    means = []
    standard_deviations = []

    for policy in POLICY_ORDER:
        values = [
            float(row[metric["column"]])
            for row in results[policy]
        ]

        mean_value = sum(values) / len(values)

        # Population standard deviation, consistent with
        # the existing statistical summary.
        variance = sum(
            (value - mean_value) ** 2
            for value in values
        ) / len(values)

        standard_deviation = variance ** 0.5

        means.append(mean_value)
        standard_deviations.append(standard_deviation)

    # Deadline success is easier to read as a percentage.
    if metric["column"] == "deadline_success_rate":
        means = [value * 100 for value in means]
        standard_deviations = [
            value * 100 for value in standard_deviations
        ]

    fig, ax = plt.subplots(figsize=(9, 5.5))

    bars = ax.bar(
        [POLICY_LABELS[policy] for policy in POLICY_ORDER],
        means,
        yerr=standard_deviations,
        capsize=5,
        edgecolor="black",
        linewidth=0.7,
    )

    ax.set_title(metric["title"], pad=14)
    ax.set_ylabel(metric["ylabel"])
    ax.set_xlabel("Scheduling policy")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)

    # Add a small amount of space above the error bars.
    upper_values = [
        mean + std
        for mean, std in zip(means, standard_deviations)
    ]
    lower_values = [
        mean - std
        for mean, std in zip(means, standard_deviations)
    ]

    upper = max(upper_values)
    lower = min(lower_values)

    if lower >= 0:
        ax.set_ylim(bottom=0)

    ax.set_ylim(
        bottom=ax.get_ylim()[0],
        top=upper + max((upper - lower) * 0.18, 0.5),
    )

    for bar, mean_value in zip(bars, means):
        ax.annotate(
            f"{mean_value:.2f}",
            (
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
            ),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()

    output_path = OUTPUT_DIR / metric["filename"]

    fig.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"Created: {output_path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = load_data()

    print(f"Input: {INPUT_FILE}")
    print(f"Episodes per policy: {len(results[POLICY_ORDER[0]])}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    for metric in METRICS:
        plot_metric(results, metric)

    print()
    print("All three figures created successfully.")
    print(
        "Error bars show population standard deviation "
        "across simulation episodes, not confidence intervals."
    )


if __name__ == "__main__":
    main()