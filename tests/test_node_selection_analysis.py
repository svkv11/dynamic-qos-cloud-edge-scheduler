from experiments.experiment_runner import ExperimentRunner
from experiments.node_selection_analysis import NodeSelectionAnalyzer


print("=" * 80)
print("NODE SELECTION ANALYSIS TEST")
print("=" * 80)

runner = ExperimentRunner()
analyzer = NodeSelectionAnalyzer()

print()
print("Running All Experiment Scenarios")

scenario_names = [
    "normal",
    "high_cpu",
    "high_memory",
    "high_latency"
]

results = {}

for scenario_name in scenario_names:
    results[scenario_name] = runner.run_experiment(
        scenario_name
    )

print(
    f"Scenarios Completed: "
    f"{len(results)}"
)

print()
print("Building Node Selection Matrix")

selection_matrix = analyzer.build_selection_matrix(
    results
)

analyzer.display_selection_matrix(
    selection_matrix
)

print()
print("Analyzing Selection Changes")

changed_tasks = analyzer.get_changed_tasks(
    selection_matrix
)

change_count = analyzer.get_selection_change_count(
    selection_matrix
)

analyzer.display_changed_tasks(
    changed_tasks
)

print()
print("Calculating Adaptation Rate")

adaptation_rate = (
    analyzer.get_selection_adaptation_rate(
        selection_matrix
    )
)

analyzer.display_adaptation_rate(
    selection_matrix
)

print()
print(
    f"Tasks With Selection Changes: "
    f"{change_count}"
)

print(
    f"Node Selection Adaptation Rate: "
    f"{adaptation_rate}%"
)

print()
print("=" * 80)
print("TEST RESULT")
print("=" * 80)

correct_scenario_count = (
    len(results) == 4
)

correct_task_count = (
    len(selection_matrix) == 4
)

correct_change_count = (
    change_count == 3
)

correct_adaptation_rate = (
    adaptation_rate == 75.0
)

if (
    correct_scenario_count
    and correct_task_count
    and correct_change_count
    and correct_adaptation_rate
):
    print("Node Selection Analysis Test: PASSED")
else:
    print("Node Selection Analysis Test: FAILED")

print("=" * 80)