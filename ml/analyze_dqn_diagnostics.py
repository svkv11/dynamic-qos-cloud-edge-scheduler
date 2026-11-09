
import csv
import os
import json
from collections import defaultdict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "experiments",
    "results",
    "dqn_diagnostics",
    "dqn_task_level_diagnostics.csv",
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "experiments",
    "results",
    "dqn_diagnostics",
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "dqn_performance_by_workload_and_node.csv",
)

CHOICE_FILE = os.path.join(
    OUTPUT_DIR,
    "dqn_choice_analysis.json",
)


def mean(values):
    return sum(values) / len(values) if values else 0.0


def main():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    if os.path.exists(OUTPUT_FILE) or os.path.exists(CHOICE_FILE):
        raise FileExistsError(
            "An analysis output already exists. "
            "No existing file has been overwritten."
        )

    groups = defaultdict(list)
    choice_groups = defaultdict(list)
    workload_totals = defaultdict(int)

    total_tasks = 0
    cloud_selected_with_alternatives = 0
    cloud_tasks_with_alternatives = 0
    cloud_selected_as_only_valid = 0

    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "workload_type",
            "selected_node",
            "simulated_execution_time",
            "deadline_met",
            "qos_score",
            "valid_action_count",
            "valid_actions",
            "gpu_required",
        }

        missing = required_columns - set(reader.fieldnames or [])

        if missing:
            raise ValueError(f"Missing CSV columns: {sorted(missing)}")

        for row in reader:
            total_tasks += 1

            workload = row["workload_type"]
            node = row["selected_node"]

            execution_time = float(row["simulated_execution_time"])
            qos = float(row["qos_score"])
            deadline_met = int(row["deadline_met"])
            valid_count = int(row["valid_action_count"])

            groups[(workload, node)].append({
                "execution_time": execution_time,
                "qos": qos,
                "deadline_met": deadline_met,
            })

            workload_totals[workload] += 1

            choice_groups[(workload, valid_count)].append(row)

            if node == "cloud-01":
                if valid_count == 1:
                    cloud_selected_as_only_valid += 1
                else:
                    cloud_tasks_with_alternatives += 1
                    cloud_selected_with_alternatives += 1

    # Generate workload and node performance summary.
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "workload_type",
            "selected_node",
            "task_count",
            "mean_simulated_execution_time",
            "mean_qos_score",
            "deadline_success_percentage",
        ])

        for workload, node in sorted(groups):
            records = groups[(workload, node)]

            writer.writerow([
                workload,
                node,
                len(records),
                round(mean([r["execution_time"] for r in records]), 4),
                round(mean([r["qos"] for r in records]), 4),
                round(
                    mean([r["deadline_met"] for r in records]) * 100,
                    2,
                ),
            ])

    # Analyse node choices according to the number of valid actions.
    choice_summary = {}

    for (workload, valid_count), records in sorted(choice_groups.items()):
        selected_counts = defaultdict(int)

        for row in records:
            selected_counts[row["selected_node"]] += 1

        key = f"{workload}_valid_actions_{valid_count}"

        choice_summary[key] = {
            "workload_type": workload,
            "valid_action_count": valid_count,
            "task_count": len(records),
            "selected_node_counts": dict(selected_counts),
        }

    summary = {
        "total_tasks": total_tasks,
        "workload_totals": dict(workload_totals),
        "cloud_selected_as_only_valid_node": cloud_selected_as_only_valid,
        "cloud_selected_when_alternatives_available":
            cloud_selected_with_alternatives,
        "cloud_tasks_with_alternatives":
            cloud_tasks_with_alternatives,
        "workload_valid_action_analysis": choice_summary,
        "performance_summary_file": os.path.relpath(
            OUTPUT_FILE, PROJECT_ROOT
        ),
    }

    with open(CHOICE_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    print("\nDQN performance analysis completed.")
    print(f"Total tasks analysed: {total_tasks}")
    print(
        "Cloud selected when it was the only valid node:",
        cloud_selected_as_only_valid,
    )
    print(
        "Cloud selected when alternatives were available:",
        cloud_selected_with_alternatives,
    )

    print("\nSaved files:")
    print(OUTPUT_FILE)
    print(CHOICE_FILE)


if __name__ == "__main__":
    main()
