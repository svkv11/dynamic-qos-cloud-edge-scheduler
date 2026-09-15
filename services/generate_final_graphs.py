import csv
import os

import matplotlib.pyplot as plt


RESULTS_DIR = os.path.join(
    "experiments",
    "results"
)

CSV_FILE = os.path.join(
    RESULTS_DIR,
    "final_stress_results.csv"
)


# ---------------------------------------------------------
# LOAD FINAL RESULTS
# ---------------------------------------------------------

results = []

with open(
    CSV_FILE,
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        results.append({
            "scenario": row["scenario"],
            "scheduler": row["scheduler"],
            "average_execution_time": float(
                row["average_execution_time"]
            ),
            "average_qos": float(
                row["average_qos"]
            ),
            "deadline_success_rate": float(
                row["deadline_success_rate"]
            )
        })


scenarios = []

for row in results:
    if row["scenario"] not in scenarios:
        scenarios.append(row["scenario"])


schedulers = [
    "Round Robin",
    "Resource Only",
    "GenAI + Dynamic QoS"
]


# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def get_values(metric, scenario):
    values = []

    for scheduler in schedulers:

        matching_rows = [
            row
            for row in results
            if row["scenario"] == scenario
            and row["scheduler"] == scheduler
        ]

        if matching_rows:
            values.append(
                matching_rows[0][metric]
            )
        else:
            values.append(0)

    return values


# ---------------------------------------------------------
# GRAPH 1 — EXECUTION TIME
# ---------------------------------------------------------

plt.figure(figsize=(12, 7))

x_positions = list(range(len(scenarios)))
width = 0.25

for index, scheduler in enumerate(schedulers):

    values = []

    for scenario in scenarios:
        matching_rows = [
            row
            for row in results
            if row["scenario"] == scenario
            and row["scheduler"] == scheduler
        ]

        values.append(
            matching_rows[0]["average_execution_time"]
        )

    positions = [
        x + (index - 1) * width
        for x in x_positions
    ]

    plt.bar(
        positions,
        values,
        width=width,
        label=scheduler
    )


plt.xlabel("Workload Scenario")
plt.ylabel("Average Execution Time (seconds)")
plt.title(
    "Execution Time Comparison Across Workload Scenarios"
)

plt.xticks(
    x_positions,
    scenarios,
    rotation=20,
    ha="right"
)

plt.legend()
plt.tight_layout()

execution_file = os.path.join(
    RESULTS_DIR,
    "final_execution_time_comparison.png"
)

plt.savefig(
    execution_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# GRAPH 2 — QoS
# ---------------------------------------------------------

plt.figure(figsize=(12, 7))

for index, scheduler in enumerate(schedulers):

    values = []

    for scenario in scenarios:
        matching_rows = [
            row
            for row in results
            if row["scenario"] == scenario
            and row["scheduler"] == scheduler
        ]

        values.append(
            matching_rows[0]["average_qos"]
        )

    positions = [
        x + (index - 1) * width
        for x in x_positions
    ]

    plt.bar(
        positions,
        values,
        width=width,
        label=scheduler
    )


plt.xlabel("Workload Scenario")
plt.ylabel("Average QoS Score")
plt.title(
    "QoS Comparison Across Workload Scenarios"
)

plt.xticks(
    x_positions,
    scenarios,
    rotation=20,
    ha="right"
)

plt.ylim(
    0,
    100
)

plt.legend()
plt.tight_layout()

qos_file = os.path.join(
    RESULTS_DIR,
    "final_qos_comparison.png"
)

plt.savefig(
    qos_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# GRAPH 3 — DEADLINE SUCCESS
# ---------------------------------------------------------

plt.figure(figsize=(12, 7))

for index, scheduler in enumerate(schedulers):

    values = []

    for scenario in scenarios:
        matching_rows = [
            row
            for row in results
            if row["scenario"] == scenario
            and row["scheduler"] == scheduler
        ]

        values.append(
            matching_rows[0]["deadline_success_rate"]
        )

    positions = [
        x + (index - 1) * width
        for x in x_positions
    ]

    plt.bar(
        positions,
        values,
        width=width,
        label=scheduler
    )


plt.xlabel("Workload Scenario")
plt.ylabel("Deadline Success Rate (%)")
plt.title(
    "Deadline Success Comparison Across Workload Scenarios"
)

plt.xticks(
    x_positions,
    scenarios,
    rotation=20,
    ha="right"
)

plt.ylim(
    0,
    100
)

plt.legend()
plt.tight_layout()

deadline_file = os.path.join(
    RESULTS_DIR,
    "final_deadline_success_comparison.png"
)

plt.savefig(
    deadline_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# GRAPH 4 — OVERALL COMPARISON
# ---------------------------------------------------------

overall_csv = os.path.join(
    RESULTS_DIR,
    "final_overall_comparison.csv"
)

overall_results = []

with open(
    overall_csv,
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        overall_results.append({
            "scheduler": row["scheduler"],
            "average_execution_time": float(
                row["average_execution_time"]
            ),
            "average_qos": float(
                row["average_qos"]
            ),
            "deadline_success_rate": float(
                row["deadline_success_rate"]
            )
        })


overall_schedulers = [
    row["scheduler"]
    for row in overall_results
]

overall_times = [
    row["average_execution_time"]
    for row in overall_results
]

overall_qos = [
    row["average_qos"]
    for row in overall_results
]

overall_deadlines = [
    row["deadline_success_rate"]
    for row in overall_results
]


plt.figure(figsize=(10, 7))

x = list(range(len(overall_schedulers)))

plt.bar(
    x,
    overall_times
)

plt.xlabel("Scheduler")
plt.ylabel("Average Execution Time (seconds)")
plt.title(
    "Overall Average Execution Time"
)

plt.xticks(
    x,
    overall_schedulers,
    rotation=15,
    ha="right"
)

plt.tight_layout()

overall_time_file = os.path.join(
    RESULTS_DIR,
    "final_overall_execution_time.png"
)

plt.savefig(
    overall_time_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# FINAL MESSAGE
# ---------------------------------------------------------

print()
print("=" * 80)
print("STEP 19 - FINAL RESULT VISUALIZATION")
print("=" * 80)

print()
print("Graphs created successfully:")
print()

print(
    f"1. {execution_file}"
)

print(
    f"2. {qos_file}"
)

print(
    f"3. {deadline_file}"
)

print(
    f"4. {overall_time_file}"
)

print()
print("=" * 80)
print("STEP 19 COMPLETED SUCCESSFULLY")
print("=" * 80)