import csv
import os

import matplotlib.pyplot as plt


RESULTS_DIR = os.path.join(
    "experiments",
    "results"
)

CSV_FILE = os.path.join(
    RESULTS_DIR,
    "genai_stress_results.csv"
)

EXECUTION_GRAPH = os.path.join(
    RESULTS_DIR,
    "execution_time_comparison.png"
)

QOS_GRAPH = os.path.join(
    RESULTS_DIR,
    "qos_comparison.png"
)

DEADLINE_GRAPH = os.path.join(
    RESULTS_DIR,
    "deadline_success_comparison.png"
)

SUMMARY_GRAPH = os.path.join(
    RESULTS_DIR,
    "scheduler_comparison.png"
)


RESULTS = [
    {
        "scenario": "Normal Mixed Workload",
        "scheduler": "Round Robin",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 13.66,
        "average_qos": 70.81
    },
    {
        "scenario": "Normal Mixed Workload",
        "scheduler": "Resource Only",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 13.06,
        "average_qos": 73.53
    },
    {
        "scenario": "Normal Mixed Workload",
        "scheduler": "GenAI + Dynamic QoS",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 9.32,
        "average_qos": 87.80
    },

    {
        "scenario": "High CPU Pressure",
        "scheduler": "Round Robin",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 16.65,
        "average_qos": 72.37
    },
    {
        "scenario": "High CPU Pressure",
        "scheduler": "Resource Only",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 20.21,
        "average_qos": 73.11
    },
    {
        "scenario": "High CPU Pressure",
        "scheduler": "GenAI + Dynamic QoS",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 13.09,
        "average_qos": 85.56
    },

    {
        "scenario": "High Memory Pressure",
        "scheduler": "Round Robin",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 23.40,
        "average_qos": 68.66
    },
    {
        "scenario": "High Memory Pressure",
        "scheduler": "Resource Only",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 23.40,
        "average_qos": 68.66
    },
    {
        "scenario": "High Memory Pressure",
        "scheduler": "GenAI + Dynamic QoS",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 23.40,
        "average_qos": 66.90
    },

    {
        "scenario": "GPU Heavy",
        "scheduler": "Round Robin",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 10.75,
        "average_qos": 68.54
    },
    {
        "scenario": "GPU Heavy",
        "scheduler": "Resource Only",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 6.90,
        "average_qos": 68.82
    },
    {
        "scenario": "GPU Heavy",
        "scheduler": "GenAI + Dynamic QoS",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 6.90,
        "average_qos": 88.40
    },

    {
        "scenario": "Tight Deadlines",
        "scheduler": "Round Robin",
        "total_tasks": 10,
        "completed_tasks": 6,
        "failed_tasks": 4,
        "deadline_success_rate": 60.0,
        "average_execution_time": 11.42,
        "average_qos": 77.24
    },
    {
        "scenario": "Tight Deadlines",
        "scheduler": "Resource Only",
        "total_tasks": 10,
        "completed_tasks": 8,
        "failed_tasks": 2,
        "deadline_success_rate": 80.0,
        "average_execution_time": 9.98,
        "average_qos": 80.22
    },
    {
        "scenario": "Tight Deadlines",
        "scheduler": "GenAI + Dynamic QoS",
        "total_tasks": 10,
        "completed_tasks": 8,
        "failed_tasks": 2,
        "deadline_success_rate": 80.0,
        "average_execution_time": 8.01,
        "average_qos": 94.15
    },

    {
        "scenario": "Priority Conflict",
        "scheduler": "Round Robin",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 12.95,
        "average_qos": 75.06
    },
    {
        "scenario": "Priority Conflict",
        "scheduler": "Resource Only",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 11.63,
        "average_qos": 76.29
    },
    {
        "scenario": "Priority Conflict",
        "scheduler": "GenAI + Dynamic QoS",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 8.73,
        "average_qos": 88.31
    }
]


def create_results_directory():
    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )


def save_csv():
    fieldnames = [
        "scenario",
        "scheduler",
        "total_tasks",
        "completed_tasks",
        "failed_tasks",
        "deadline_success_rate",
        "average_execution_time",
        "average_qos"
    ]

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for result in RESULTS:
            writer.writerow(result)

    print(f"CSV created: {CSV_FILE}")


def get_scenario_data(scenario):
    return [
        result
        for result in RESULTS
        if result["scenario"] == scenario
    ]


def create_execution_time_graph():
    scenarios = list(
        dict.fromkeys(
            result["scenario"]
            for result in RESULTS
        )
    )

    schedulers = [
        "Round Robin",
        "Resource Only",
        "GenAI + Dynamic QoS"
    ]

    for scheduler in schedulers:

        values = []

        for scenario in scenarios:

            matching = [
                result
                for result in RESULTS
                if (
                    result["scenario"] == scenario
                    and result["scheduler"] == scheduler
                )
            ]

            values.append(
                matching[0]["average_execution_time"]
            )

        plt.plot(
            scenarios,
            values,
            marker="o",
            label=scheduler
        )

    plt.title(
        "Average Execution Time Comparison"
    )

    plt.xlabel("Stress Scenario")
    plt.ylabel("Average Execution Time (seconds)")

    plt.xticks(
        rotation=25,
        ha="right"
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        EXECUTION_GRAPH,
        dpi=300
    )

    plt.close()

    print(
        f"Graph created: {EXECUTION_GRAPH}"
    )


def create_qos_graph():
    scenarios = list(
        dict.fromkeys(
            result["scenario"]
            for result in RESULTS
        )
    )

    schedulers = [
        "Round Robin",
        "Resource Only",
        "GenAI + Dynamic QoS"
    ]

    for scheduler in schedulers:

        values = []

        for scenario in scenarios:

            matching = [
                result
                for result in RESULTS
                if (
                    result["scenario"] == scenario
                    and result["scheduler"] == scheduler
                )
            ]

            values.append(
                matching[0]["average_qos"]
            )

        plt.plot(
            scenarios,
            values,
            marker="o",
            label=scheduler
        )

    plt.title(
        "Average QoS Score Comparison"
    )

    plt.xlabel("Stress Scenario")
    plt.ylabel("Average QoS Score")

    plt.xticks(
        rotation=25,
        ha="right"
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        QOS_GRAPH,
        dpi=300
    )

    plt.close()

    print(
        f"Graph created: {QOS_GRAPH}"
    )


def create_deadline_graph():
    scenarios = list(
        dict.fromkeys(
            result["scenario"]
            for result in RESULTS
        )
    )

    schedulers = [
        "Round Robin",
        "Resource Only",
        "GenAI + Dynamic QoS"
    ]

    for scheduler in schedulers:

        values = []

        for scenario in scenarios:

            matching = [
                result
                for result in RESULTS
                if (
                    result["scenario"] == scenario
                    and result["scheduler"] == scheduler
                )
            ]

            values.append(
                matching[0]["deadline_success_rate"]
            )

        plt.plot(
            scenarios,
            values,
            marker="o",
            label=scheduler
        )

    plt.title(
        "Deadline Success Rate Comparison"
    )

    plt.xlabel("Stress Scenario")
    plt.ylabel("Deadline Success Rate (%)")

    plt.xticks(
        rotation=25,
        ha="right"
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        DEADLINE_GRAPH,
        dpi=300
    )

    plt.close()

    print(
        f"Graph created: {DEADLINE_GRAPH}"
    )


def create_summary_graph():
    scenarios = list(
        dict.fromkeys(
            result["scenario"]
            for result in RESULTS
        )
    )

    genai_values = []
    resource_values = []
    round_robin_values = []

    for scenario in scenarios:

        scenario_results = get_scenario_data(
            scenario
        )

        for result in scenario_results:

            if result["scheduler"] == "GenAI + Dynamic QoS":
                genai_values.append(
                    result["average_qos"]
                )

            elif result["scheduler"] == "Resource Only":
                resource_values.append(
                    result["average_qos"]
                )

            elif result["scheduler"] == "Round Robin":
                round_robin_values.append(
                    result["average_qos"]
                )

    x_positions = range(
        len(scenarios)
    )

    width = 0.25

    plt.bar(
        [
            x - width
            for x in x_positions
        ],
        round_robin_values,
        width=width,
        label="Round Robin"
    )

    plt.bar(
        x_positions,
        resource_values,
        width=width,
        label="Resource Only"
    )

    plt.bar(
        [
            x + width
            for x in x_positions
        ],
        genai_values,
        width=width,
        label="GenAI + Dynamic QoS"
    )

    plt.title(
        "QoS Comparison Across Stress Scenarios"
    )

    plt.xlabel("Stress Scenario")
    plt.ylabel("Average QoS Score")

    plt.xticks(
        list(x_positions),
        scenarios,
        rotation=25,
        ha="right"
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        SUMMARY_GRAPH,
        dpi=300
    )

    plt.close()

    print(
        f"Graph created: {SUMMARY_GRAPH}"
    )


def main():
    print("=" * 60)
    print("STEP 16 - STRESS RESULTS EXPORT")
    print("=" * 60)

    create_results_directory()

    save_csv()

    create_execution_time_graph()

    create_qos_graph()

    create_deadline_graph()

    create_summary_graph()

    print("=" * 60)
    print("STEP 16 COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()