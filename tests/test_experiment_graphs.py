import os

from experiments.experiment_graphs import ExperimentGraphs


graphs = ExperimentGraphs()

print("=" * 60)
print("EXPERIMENT GRAPH GENERATION TEST")
print("=" * 60)

csv_path = (
    "experiments/results/"
    "experiment_comparison.csv"
)

output_path = (
    "experiments/results/"
    "node_usage.png"
)

print()
print("Loading Experiment Results")

results = graphs.load_results(csv_path)

print(
    f"Scenarios Loaded: {len(results)}"
)

print()
print("Generating Node Usage Graph")

generated_path = graphs.plot_node_usage(
    csv_path,
    output_path
)

print(
    f"Graph Generated: {generated_path}"
)

print()
print("Checking Graph File")

file_exists = os.path.exists(generated_path)

print(
    f"Graph File Exists: {file_exists}"
)

if file_exists:
    file_size = os.path.getsize(generated_path)

    print(
        f"Graph File Size: {file_size} bytes"
    )

print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)

correct_scenario_count = (
    len(results) == 4
)

valid_file = (
    file_exists
    and os.path.getsize(generated_path) > 0
)

if (
    correct_scenario_count
    and valid_file
):
    print("Node Usage Graph Test: PASSED")
else:
    print("Node Usage Graph Test: FAILED")

print("=" * 60)