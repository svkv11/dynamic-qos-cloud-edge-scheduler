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
print("Calculating Overall Adaptation Rate")

adaptation_rate = (
    analyzer.get_selection_adaptation_rate(
        selection_matrix
    )
)

analyzer.display_adaptation_rate(
    selection_matrix
)

print()
print("Comparing Resource Scenarios")

scenario_comparisons = [
    ("normal", "high_cpu"),
    ("normal", "high_memory"),
    ("normal", "high_latency")
]

comparison_results = {}

for base_scenario, comparison_scenario in (
    scenario_comparisons
):

    comparison = analyzer.compare_scenarios(
        selection_matrix,
        base_scenario,
        comparison_scenario
    )

    comparison_results[
        f"{base_scenario}_to_{comparison_scenario}"
    ] = comparison

    analyzer.display_scenario_comparison(
        comparison,
        base_scenario,
        comparison_scenario
    )

    scenario_change_count = (
        analyzer.get_scenario_change_count(
            comparison
        )
    )

    scenario_adaptation_rate = (
        analyzer.get_scenario_adaptation_rate(
            comparison
        )
    )

    print(
        f"Changed Tasks: "
        f"{scenario_change_count}"
    )

    print(
        f"Adaptation Rate: "
        f"{scenario_adaptation_rate}%"
    )

print()
print("=" * 80)
print("VALIDATION DETAILS")
print("=" * 80)

normal_to_high_cpu = comparison_results[
    "normal_to_high_cpu"
]

normal_to_high_memory = comparison_results[
    "normal_to_high_memory"
]

normal_to_high_latency = comparison_results[
    "normal_to_high_latency"
]

checks = {
    "Scenario count == 4": (
        len(results) == 4
    ),
    "Task count == 4": (
        len(selection_matrix) == 4
    ),
    "Overall changed tasks == 3": (
        change_count == 3
    ),
    "Overall adaptation rate == 75.0": (
        adaptation_rate == 75.0
    ),
    "High CPU changed tasks == 2": (
        analyzer.get_scenario_change_count(
            normal_to_high_cpu
        ) == 2
    ),
    "High CPU adaptation rate == 50.0": (
        analyzer.get_scenario_adaptation_rate(
            normal_to_high_cpu
        ) == 50.0
    ),
    "High Memory changed tasks == 3": (
        analyzer.get_scenario_change_count(
            normal_to_high_memory
        ) == 3
    ),
    "High Memory adaptation rate == 75.0": (
        analyzer.get_scenario_adaptation_rate(
            normal_to_high_memory
        ) == 75.0
    ),
    "High Latency changed tasks == 2": (
        analyzer.get_scenario_change_count(
            normal_to_high_latency
        ) == 2
    ),
    "High Latency adaptation rate == 50.0": (
        analyzer.get_scenario_adaptation_rate(
            normal_to_high_latency
        ) == 50.0
    )
}

for check_name, check_result in checks.items():
    status = "PASS" if check_result else "FAIL"

    print(
        f"{status:<6} | "
        f"{check_name}"
    )

print()
print("=" * 80)
print("TEST RESULT")
print("=" * 80)

if all(checks.values()):
    print(
        "Node Selection Analysis Test: PASSED"
    )
else:
    print(
        "Node Selection Analysis Test: FAILED"
    )

print("=" * 80)