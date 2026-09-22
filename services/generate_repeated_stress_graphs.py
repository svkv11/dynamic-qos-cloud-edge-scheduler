import csv
import os
import statistics

import matplotlib.pyplot as plt


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RESULTS_DIR = os.path.join(
    PROJECT_ROOT,
    "experiments",
    "results"
)

INPUT_CSV = os.path.join(
    RESULTS_DIR,
    "genai_stress_repeated_results.csv"
)

OUTPUT_DIR = os.path.join(
    RESULTS_DIR,
    "repeated_figures"
)


SCENARIOS = [
    "Normal Mixed Workload",
    "High CPU Pressure",
    "High Memory Pressure",
    "GPU Heavy",
    "Tight Deadlines",
    "Priority Conflict"
]

SCHEDULERS = [
    "Round Robin",
    "Resource Only",
    "GenAI + QoS"
]


def load_results():

    rows = []

    with open(
        INPUT_CSV,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            rows.append({
                "repetition": int(
                    row["repetition"]
                ),
                "scenario": row["scenario"],
                "scheduler": row["scheduler"],
                "execution_time": float(
                    row["average_execution_time"]
                ),
                "qos": float(
                    row["average_qos"]
                ),
                "deadline_success": float(
                    row["deadline_success_rate"]
                )
            })

    return rows


def mean_std(values):

    if not values:
        return 0.0, 0.0

    mean_value = statistics.mean(
        values
    )

    if len(values) > 1:
        std_value = statistics.stdev(
            values
        )
    else:
        std_value = 0.0

    return mean_value, std_value


def aggregate_by_scenario(
    rows,
    metric
):

    data = {}

    for scenario in SCENARIOS:

        data[scenario] = {}

        for scheduler in SCHEDULERS:

            values = [
                row[metric]
                for row in rows
                if row["scenario"] == scenario
                and row["scheduler"] == scheduler
            ]

            mean_value, std_value = mean_std(
                values
            )

            data[scenario][scheduler] = (
                mean_value,
                std_value
            )

    return data


def create_execution_time_graph(
    rows
):

    data = aggregate_by_scenario(
        rows,
        "execution_time"
    )

    x_positions = range(
        len(SCENARIOS)
    )

    width = 0.25

    plt.figure(
        figsize=(13, 7)
    )

    for index, scheduler in enumerate(
        SCHEDULERS
    ):

        means = [
            data[scenario][scheduler][0]
            for scenario in SCENARIOS
        ]

        stds = [
            data[scenario][scheduler][1]
            for scenario in SCENARIOS
        ]

        positions = [
            x + (
                index - 1
            ) * width
            for x in x_positions
        ]

        plt.bar(
            positions,
            means,
            width=width,
            yerr=stds,
            capsize=4,
            label=scheduler
        )

    plt.xticks(
        list(x_positions),
        SCENARIOS,
        rotation=20,
        ha="right"
    )

    plt.ylabel(
        "Average Execution Time (seconds)"
    )

    plt.xlabel(
        "Workload Scenario"
    )

    plt.title(
        "Execution Time Across Repeated Evaluations"
    )

    plt.legend()

    plt.tight_layout()

    output_path = os.path.join(
        OUTPUT_DIR,
        "repeated_execution_time.png"
    )

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()

    print(
        f"Graph created: {output_path}"
    )


def create_qos_graph(
    rows
):

    data = aggregate_by_scenario(
        rows,
        "qos"
    )

    x_positions = range(
        len(SCENARIOS)
    )

    width = 0.25

    plt.figure(
        figsize=(13, 7)
    )

    for index, scheduler in enumerate(
        SCHEDULERS
    ):

        means = [
            data[scenario][scheduler][0]
            for scenario in SCENARIOS
        ]

        stds = [
            data[scenario][scheduler][1]
            for scenario in SCENARIOS
        ]

        positions = [
            x + (
                index - 1
            ) * width
            for x in x_positions
        ]

        plt.bar(
            positions,
            means,
            width=width,
            yerr=stds,
            capsize=4,
            label=scheduler
        )

    plt.xticks(
        list(x_positions),
        SCENARIOS,
        rotation=20,
        ha="right"
    )

    plt.ylabel(
        "Average QoS Score"
    )

    plt.xlabel(
        "Workload Scenario"
    )

    plt.title(
        "QoS Across Repeated Evaluations"
    )

    plt.legend()

    plt.tight_layout()

    output_path = os.path.join(
        OUTPUT_DIR,
        "repeated_qos.png"
    )

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()

    print(
        f"Graph created: {output_path}"
    )


def create_deadline_graph(
    rows
):

    data = aggregate_by_scenario(
        rows,
        "deadline_success"
    )

    x_positions = range(
        len(SCENARIOS)
    )

    width = 0.25

    plt.figure(
        figsize=(13, 7)
    )

    for index, scheduler in enumerate(
        SCHEDULERS
    ):

        means = [
            data[scenario][scheduler][0]
            for scenario in SCENARIOS
        ]

        stds = [
            data[scenario][scheduler][1]
            for scenario in SCENARIOS
        ]

        positions = [
            x + (
                index - 1
            ) * width
            for x in x_positions
        ]

        plt.bar(
            positions,
            means,
            width=width,
            yerr=stds,
            capsize=4,
            label=scheduler
        )

    plt.xticks(
        list(x_positions),
        SCENARIOS,
        rotation=20,
        ha="right"
    )

    plt.ylabel(
        "Deadline Success Rate (%)"
    )

    plt.xlabel(
        "Workload Scenario"
    )

    plt.title(
        "Deadline Success Across Repeated Evaluations"
    )

    plt.ylim(
        0,
        110
    )

    plt.legend()

    plt.tight_layout()

    output_path = os.path.join(
        OUTPUT_DIR,
        "repeated_deadline_success.png"
    )

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()

    print(
        f"Graph created: {output_path}"
    )


def create_overall_graph(
    rows
):

    metrics = {
        "Execution Time": "execution_time",
        "QoS Score": "qos",
        "Deadline Success": "deadline_success"
    }

    for metric_name, metric_key in metrics.items():

        scheduler_means = []
        scheduler_stds = []

        for scheduler in SCHEDULERS:

            values = [
                row[metric_key]
                for row in rows
                if row["scheduler"] == scheduler
            ]

            mean_value, std_value = mean_std(
                values
            )

            scheduler_means.append(
                mean_value
            )

            scheduler_stds.append(
                std_value
            )

        plt.figure(
            figsize=(9, 6)
        )

        x_positions = range(
            len(SCHEDULERS)
        )

        plt.bar(
            list(x_positions),
            scheduler_means,
            yerr=scheduler_stds,
            capsize=5
        )

        plt.xticks(
            list(x_positions),
            SCHEDULERS
        )

        plt.ylabel(
            metric_name
        )

        plt.xlabel(
            "Scheduler"
        )

        plt.title(
            f"Overall {metric_name} Across Repeated Evaluations"
        )

        if metric_key == "deadline_success":
            plt.ylim(
                0,
                110
            )

        plt.tight_layout()

        filename = (
            metric_name
            .lower()
            .replace(
                " ",
                "_"
            )
            + "_overall_repeated.png"
        )

        output_path = os.path.join(
            OUTPUT_DIR,
            filename
        )

        plt.savefig(
            output_path,
            dpi=300
        )

        plt.close()

        print(
            f"Graph created: {output_path}"
        )


def main():

    print(
        "Loading repeated experiment results..."
    )

    if not os.path.exists(
        INPUT_CSV
    ):
        raise FileNotFoundError(
            f"Input file not found: {INPUT_CSV}"
        )

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    rows = load_results()

    print(
        f"Loaded {len(rows)} repeated experiment records."
    )

    create_execution_time_graph(
        rows
    )

    create_qos_graph(
        rows
    )

    create_deadline_graph(
        rows
    )

    create_overall_graph(
        rows
    )

    print()
    print(
        "All repeated-experiment graphs generated successfully."
    )


if __name__ == "__main__":
    main()