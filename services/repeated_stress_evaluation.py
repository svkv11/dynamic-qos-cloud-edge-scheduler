import csv
import os
import statistics

from services.genai_stress_evaluation import run_scenario


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

REPEATED_RESULTS_CSV = os.path.join(
    RESULTS_DIR,
    "genai_stress_repeated_results.csv"
)

REPEATED_SUMMARY_CSV = os.path.join(
    RESULTS_DIR,
    "genai_stress_repeated_summary.csv"
)

NUM_REPETITIONS = 5


SCENARIOS = {
    "Normal Mixed Workload": [
        "Create an AI image quickly.",
        "Analyze a large dataset.",
        "Process a CPU-heavy workload.",
        "Run a deep learning model using GPU.",
        "Run a normal data processing task.",
        "Analyze a large memory-intensive dataset.",
        "Run an urgent AI workload.",
        "Process a CPU-intensive computation.",
        "Generate an AI image using GPU.",
        "Run a normal workload."
    ],

    "High CPU Pressure": [
        "Process a CPU-heavy workload using 6 CPU cores.",
        "Run a CPU-intensive computation.",
        "Perform heavy CPU processing.",
        "Execute a CPU-heavy data analysis task.",
        "Run a CPU-intensive workload.",
        "Process a workload requiring high CPU.",
        "Perform intensive CPU computation.",
        "Run another CPU-heavy task.",
        "Execute heavy CPU processing.",
        "Process a high CPU workload."
    ],

    "High Memory Pressure": [
        "Analyze a very large dataset that requires a lot of RAM.",
        "Process a memory-intensive dataset.",
        "Run a large RAM-intensive analysis.",
        "Analyze a very large memory workload.",
        "Process a workload requiring high memory.",
        "Run a memory-intensive computation.",
        "Analyze a large dataset with high RAM usage.",
        "Process a large memory workload.",
        "Run another RAM-intensive task.",
        "Analyze a high-memory dataset."
    ],

    "GPU Heavy": [
        "Create an AI image quickly.",
        "Run a deep learning model using GPU.",
        "Perform GPU-accelerated machine learning.",
        "Generate an AI image using GPU.",
        "Run a neural network training workload using GPU.",
        "Perform GPU-intensive deep learning.",
        "Run an AI inference workload using GPU.",
        "Generate an image with GPU acceleration.",
        "Run a GPU-intensive model.",
        "Perform deep learning using GPU."
    ],

    "Tight Deadlines": [
        "Run the deep learning model using GPU within 8 seconds.",
        "Process the CPU workload within 10 seconds.",
        "Analyze the dataset within 12 seconds.",
        "Create the AI image within 8 seconds.",
        "Run the urgent GPU workload within 10 seconds.",
        "Process the task within 12 seconds.",
        "Run the deep learning task within 9 seconds.",
        "Complete the CPU-heavy task within 10 seconds.",
        "Analyze the memory-intensive workload within 12 seconds.",
        "Finish the AI workload within 8 seconds."
    ],

    "Priority Conflict": [
        "Run this task urgently using CPU.",
        "Run the GPU workload urgently.",
        "Analyze the large dataset with high priority.",
        "Process this CPU-heavy workload normally.",
        "Run the deep learning workload as soon as possible.",
        "Perform the memory-intensive task urgently.",
        "Run this normal workload with low priority.",
        "Process the CPU task urgently.",
        "Run the GPU task with critical priority.",
        "Analyze this dataset normally."
    ]
}


def save_repeated_results(rows):
    """
    Save every repetition/scenario/scheduler result.
    """

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    fieldnames = [
        "repetition",
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
        REPEATED_RESULTS_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(rows)

    print()
    print(
        f"Repeated results saved to:"
    )
    print(
        REPEATED_RESULTS_CSV
    )


def calculate_mean(values):
    if not values:
        return 0.0

    return round(
        statistics.mean(values),
        2
    )


def calculate_std(values):
    if len(values) < 2:
        return 0.0

    return round(
        statistics.stdev(values),
        2
    )


def generate_overall_summary(rows):
    """
    Calculate mean and standard deviation across
    repetitions and scenarios for each scheduler.
    """

    schedulers = [
        "Round Robin",
        "Resource Only",
        "GenAI + QoS"
    ]

    summary_rows = []

    for scheduler in schedulers:

        scheduler_rows = [
            row
            for row in rows
            if row["scheduler"] == scheduler
        ]

        execution_times = [
            float(row["average_execution_time"])
            for row in scheduler_rows
        ]

        qos_scores = [
            float(row["average_qos"])
            for row in scheduler_rows
        ]

        deadline_rates = [
            float(row["deadline_success_rate"])
            for row in scheduler_rows
        ]

        summary_rows.append({
            "scheduler": scheduler,

            "observations": len(
                scheduler_rows
            ),

            "mean_execution_time": calculate_mean(
                execution_times
            ),

            "std_execution_time": calculate_std(
                execution_times
            ),

            "mean_qos": calculate_mean(
                qos_scores
            ),

            "std_qos": calculate_std(
                qos_scores
            ),

            "mean_deadline_success_rate": calculate_mean(
                deadline_rates
            ),

            "std_deadline_success_rate": calculate_std(
                deadline_rates
            )
        })

    return summary_rows


def save_summary(summary_rows):
    """
    Save aggregate mean/std results.
    """

    fieldnames = [
        "scheduler",
        "observations",
        "mean_execution_time",
        "std_execution_time",
        "mean_qos",
        "std_qos",
        "mean_deadline_success_rate",
        "std_deadline_success_rate"
    ]

    with open(
        REPEATED_SUMMARY_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            summary_rows
        )

    print()
    print(
        "Repeated summary saved to:"
    )
    print(
        REPEATED_SUMMARY_CSV
    )


def print_final_summary(summary_rows):
    """
    Display mean +/- standard deviation.
    """

    print()
    print("=" * 115)
    print(
        "REPEATED EXPERIMENT SUMMARY"
    )
    print("=" * 115)

    print(
        f"{'Scheduler':<22}"
        f"{'Execution Time':<25}"
        f"{'QoS Score':<22}"
        f"{'Deadline Success':<25}"
    )

    print("-" * 115)

    for row in summary_rows:

        execution_text = (
            f"{row['mean_execution_time']:.2f}"
            f" +/- "
            f"{row['std_execution_time']:.2f}"
        )

        qos_text = (
            f"{row['mean_qos']:.2f}"
            f" +/- "
            f"{row['std_qos']:.2f}"
        )

        deadline_text = (
            f"{row['mean_deadline_success_rate']:.2f}%"
            f" +/- "
            f"{row['std_deadline_success_rate']:.2f}"
        )

        print(
            f"{row['scheduler']:<22}"
            f"{execution_text:<25}"
            f"{qos_text:<22}"
            f"{deadline_text:<25}"
        )

    print("=" * 115)


def main():

    print()
    print("=" * 115)
    print(
        "REPEATED GENAI STRESS EVALUATION"
    )
    print("=" * 115)

    print()
    print(
        f"Number of repetitions: "
        f"{NUM_REPETITIONS}"
    )

    print(
        f"Number of scenarios: "
        f"{len(SCENARIOS)}"
    )

    print(
        "Each repetition executes all "
        "6 scenarios using the existing "
        "Round Robin, Resource Only, "
        "and GenAI + Dynamic QoS schedulers."
    )

    all_rows = []

    for repetition in range(
        1,
        NUM_REPETITIONS + 1
    ):

        print()
        print("#" * 115)
        print(
            f"REPETITION {repetition} "
            f"OF {NUM_REPETITIONS}"
        )
        print("#" * 115)

        for scenario_name, requests in SCENARIOS.items():

            summaries = run_scenario(
                scenario_name,
                requests
            )

            for scheduler_name, summary in summaries.items():

                all_rows.append({
                    "repetition": repetition,
                    "scenario": scenario_name,
                    "scheduler": scheduler_name,
                    "total_tasks": summary["total"],
                    "completed_tasks": summary["completed"],
                    "failed_tasks": summary["failed"],
                    "deadline_success_rate": summary[
                        "deadline_rate"
                    ],
                    "average_execution_time": summary[
                        "average_execution_time"
                    ],
                    "average_qos": summary[
                        "average_qos"
                    ]
                })

        print()
        print(
            f"Repetition {repetition} completed."
        )

    save_repeated_results(
        all_rows
    )

    summary_rows = generate_overall_summary(
        all_rows
    )

    save_summary(
        summary_rows
    )

    print_final_summary(
        summary_rows
    )

    print()
    print("=" * 115)
    print(
        "REPEATED EXPERIMENT COMPLETED"
    )
    print("=" * 115)


if __name__ == "__main__":
    main()