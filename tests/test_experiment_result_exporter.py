import os

from experiments.experiment_evaluator import ExperimentEvaluator
from experiments.experiment_result_exporter import (
    ExperimentResultExporter
)


evaluator = ExperimentEvaluator()
exporter = ExperimentResultExporter()

print("=" * 60)
print("EXPERIMENT RESULT EXPORTER TEST")
print("=" * 60)

print()
print("Running All Scenarios")

results = evaluator.run_all_scenarios()

print()
print("Building Comparison")

comparison = evaluator.build_comparison(results)

print()
print("Exporting CSV")

file_path = "experiments/results/experiment_comparison.csv"

exported_path = exporter.export_csv(
    comparison,
    file_path
)

print(
    f"CSV Exported To: {exported_path}"
)

print()
print("Checking CSV File")

file_exists = os.path.exists(exported_path)

content = ""

if file_exists:
    print("CSV File Exists: True")

    with open(
        exported_path,
        "r",
        encoding="utf-8"
    ) as csv_file:
        content = csv_file.read()

    print()
    print("CSV CONTENT")
    print("-" * 60)
    print(content)
    print("-" * 60)

else:
    print("CSV File Exists: False")

print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)

expected_scenarios = {
    "normal",
    "high_cpu",
    "high_memory",
    "high_latency",
    "tight_deadline",
    "priority_conflict",
    "resource_deadline_pressure"
}

all_scenarios_present = (
    set(comparison.keys())
    == expected_scenarios
)

csv_lines = (
    content.strip().splitlines()
    if file_exists
    else []
)

correct_row_count = (
    len(csv_lines) == 8
)

header_present = (
    file_exists
    and csv_lines
    and csv_lines[0].startswith(
        "scenario,completed_tasks,failed_tasks"
    )
)

all_scenarios_exported = all(
    scenario in content
    for scenario in expected_scenarios
)

if (
    file_exists
    and all_scenarios_present
    and correct_row_count
    and header_present
    and all_scenarios_exported
):
    print("Experiment Result Exporter Test: PASSED")
else:
    print("Experiment Result Exporter Test: FAILED")

print("=" * 60)