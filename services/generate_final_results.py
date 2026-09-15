import csv
import os


RESULTS_DIR = os.path.join(
    "experiments",
    "results"
)


# ---------------------------------------------------------
# FINAL STEP 17 RESULTS
# ---------------------------------------------------------

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
        "average_execution_time": 19.00,
        "average_qos": 74.98
    },
    {
        "scenario": "High Memory Pressure",
        "scheduler": "Resource Only",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 14.60,
        "average_qos": 81.30
    },
    {
        "scenario": "High Memory Pressure",
        "scheduler": "GenAI + Dynamic QoS",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 14.60,
        "average_qos": 83.01
    },

    {
        "scenario": "GPU Heavy",
        "scheduler": "Round Robin",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 10.75,
        "average_qos": 68.74
    },
    {
        "scenario": "GPU Heavy",
        "scheduler": "Resource Only",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 6.90,
        "average_qos": 69.02
    },
    {
        "scenario": "GPU Heavy",
        "scheduler": "GenAI + Dynamic QoS",
        "total_tasks": 10,
        "completed_tasks": 10,
        "failed_tasks": 0,
        "deadline_success_rate": 100.0,
        "average_execution_time": 6.90,
        "average_qos": 88.20
    },

    {
        "scenario": "Tight Deadlines",
        "scheduler": "Round Robin",
        "total_tasks": 10,
        "completed_tasks": 6,
        "failed_tasks": 4,
        "deadline_success_rate": 60.0,
        "average_execution_time": 11.42,
        "average_qos": 77.44
    },
    {
        "scenario": "Tight Deadlines",
        "scheduler": "Resource Only",
        "total_tasks": 10,
        "completed_tasks": 8,
        "failed_tasks": 2,
        "deadline_success_rate": 80.0,
        "average_execution_time": 9.98,
        "average_qos": 80.42
    },
    {
        "scenario": "Tight Deadlines",
        "scheduler": "GenAI + Dynamic QoS",
        "total_tasks": 10,
        "completed_tasks": 8,
        "failed_tasks": 2,
        "deadline_success_rate": 80.0,
        "average_execution_time": 8.01,
        "average_qos": 93.95
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


# ---------------------------------------------------------
# CREATE RESULTS DIRECTORY
# ---------------------------------------------------------

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)


# ---------------------------------------------------------
# SAVE FINAL STRESS RESULTS
# ---------------------------------------------------------

stress_csv = os.path.join(
    RESULTS_DIR,
    "final_stress_results.csv"
)

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
    stress_csv,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(RESULTS)


# ---------------------------------------------------------
# CALCULATE OVERALL RESULTS
# ---------------------------------------------------------

schedulers = [
    "Round Robin",
    "Resource Only",
    "GenAI + Dynamic QoS"
]

overall = {}

for scheduler in schedulers:

    rows = [
        row
        for row in RESULTS
        if row["scheduler"] == scheduler
    ]

    average_execution = sum(
        row["average_execution_time"]
        for row in rows
    ) / len(rows)

    average_qos = sum(
        row["average_qos"]
        for row in rows
    ) / len(rows)

    average_deadline = sum(
        row["deadline_success_rate"]
        for row in rows
    ) / len(rows)

    total_tasks = sum(
        row["total_tasks"]
        for row in rows
    )

    completed_tasks = sum(
        row["completed_tasks"]
        for row in rows
    )

    failed_tasks = sum(
        row["failed_tasks"]
        for row in rows
    )

    overall[scheduler] = {
        "scheduler": scheduler,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks,
        "deadline_success_rate": round(
            average_deadline,
            2
        ),
        "average_execution_time": round(
            average_execution,
            2
        ),
        "average_qos": round(
            average_qos,
            2
        )
    }


# ---------------------------------------------------------
# SAVE OVERALL COMPARISON
# ---------------------------------------------------------

overall_csv = os.path.join(
    RESULTS_DIR,
    "final_overall_comparison.csv"
)

overall_fields = [
    "scheduler",
    "total_tasks",
    "completed_tasks",
    "failed_tasks",
    "deadline_success_rate",
    "average_execution_time",
    "average_qos"
]

with open(
    overall_csv,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=overall_fields
    )

    writer.writeheader()

    for scheduler in schedulers:
        writer.writerow(
            overall[scheduler]
        )


# ---------------------------------------------------------
# CALCULATE IMPROVEMENTS
# ---------------------------------------------------------

rr = overall["Round Robin"]
resource = overall["Resource Only"]
genai = overall["GenAI + Dynamic QoS"]

execution_improvement_rr = (
    (rr["average_execution_time"]
     - genai["average_execution_time"])
    / rr["average_execution_time"]
) * 100

execution_improvement_resource = (
    (resource["average_execution_time"]
     - genai["average_execution_time"])
    / resource["average_execution_time"]
) * 100

qos_improvement_rr = (
    (genai["average_qos"]
     - rr["average_qos"])
    / rr["average_qos"]
) * 100

qos_improvement_resource = (
    (genai["average_qos"]
     - resource["average_qos"])
    / resource["average_qos"]
) * 100


# ---------------------------------------------------------
# DISPLAY FINAL RESULTS
# ---------------------------------------------------------

print()
print("=" * 80)
print("STEP 18 - FINAL EXPERIMENTAL RESULTS")
print("=" * 80)

print()

print(
    f"{'Scheduler':<28}"
    f"{'Avg Time':<15}"
    f"{'Avg QoS':<15}"
    f"{'Deadline %':<15}"
)

print("-" * 73)

for scheduler in schedulers:

    result = overall[scheduler]

    print(
        f"{scheduler:<28}"
        f"{result['average_execution_time']:<15}"
        f"{result['average_qos']:<15}"
        f"{result['deadline_success_rate']:<15}"
    )


print()
print("=" * 80)
print("GENAI + DYNAMIC QoS IMPROVEMENT")
print("=" * 80)

print(
    f"Execution time improvement vs Round Robin: "
    f"{execution_improvement_rr:.2f}%"
)

print(
    f"Execution time improvement vs Resource Only: "
    f"{execution_improvement_resource:.2f}%"
)

print(
    f"QoS improvement vs Round Robin: "
    f"{qos_improvement_rr:.2f}%"
)

print(
    f"QoS improvement vs Resource Only: "
    f"{qos_improvement_resource:.2f}%"
)


print()
print("=" * 80)
print("FILES CREATED")
print("=" * 80)

print(
    f"Stress results: "
    f"{stress_csv}"
)

print(
    f"Overall comparison: "
    f"{overall_csv}"
)

print("=" * 80)
print("STEP 18 COMPLETED SUCCESSFULLY")
print("=" * 80)