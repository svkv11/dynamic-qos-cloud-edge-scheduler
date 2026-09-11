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
    "high_latency"
}

all_scenarios_present = (
    set(comparison.keys())
    == expected_scenarios
)

correct_row_count = (
    content.count("\n") == 5
    if file_exists
    else False
)

if (
    file_exists
    and all_scenarios_present
    and correct_row_count
):
    print("Experiment Result Exporter Test: PASSED")
else:
    print("Experiment Result Exporter Test: FAILED")

print("=" * 60)