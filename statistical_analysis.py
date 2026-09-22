import csv
from scipy.stats import wilcoxon


CSV_FILE = "experiments/results/genai_stress_repeated_results.csv"


def load_results():
    with open(CSV_FILE, newline="") as file:
        return list(csv.DictReader(file))


def get_values(rows, scenario, scheduler, metric):
    return [
        float(row[metric])
        for row in rows
        if row["scenario"] == scenario
        and row["scheduler"] == scheduler
    ]


def run_test(rows, baseline, metric):
    scenarios = sorted(set(row["scenario"] for row in rows))

    genai_values = []
    baseline_values = []

    for scenario in scenarios:
        genai_values.extend(
            get_values(rows, scenario, "GenAI + QoS", metric)
        )
        baseline_values.extend(
            get_values(rows, scenario, baseline, metric)
        )

    result = wilcoxon(
        genai_values,
        baseline_values,
        zero_method="wilcox",
        alternative="two-sided"
    )

    return result


def main():
    rows = load_results()

    print("WILCOXON SIGNED-RANK TEST")
    print("=" * 60)
    print()
    print("Existing experiment data only.")
    print("No experiment was rerun.")
    print()

    metrics = [
        ("average_execution_time", "Execution Time"),
        ("average_qos", "QoS Score"),
    ]

    baselines = [
        "Round Robin",
        "Resource Only",
    ]

    for baseline in baselines:
        print(f"GenAI + QoS vs {baseline}")
        print("-" * 60)

        for metric, label in metrics:
            result = run_test(rows, baseline, metric)

            print(
                f"{label}: "
                f"statistic = {result.statistic:.4f}, "
                f"p-value = {result.pvalue:.6f}"
            )

        print()


if __name__ == "__main__":
    main()