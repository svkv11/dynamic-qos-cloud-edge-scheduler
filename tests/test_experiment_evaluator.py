from experiments.experiment_evaluator import ExperimentEvaluator


evaluator = ExperimentEvaluator()

print("=" * 60)
print("EXPERIMENT EVALUATOR TEST")
print("=" * 60)

print()
print("Running All Scenarios")

results = evaluator.run_all_scenarios()

print()
print("Building Comparison")

comparison = evaluator.build_comparison(results)

print()

evaluator.display_comparison(comparison)

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

all_results_valid = all(
    result["completed_tasks"] >= 0
    and result["failed_tasks"] >= 0
    and (
        result["completed_tasks"]
        + result["failed_tasks"]
        == 4
    )
    and 0.0 <= result["deadline_success_rate"] <= 100.0
    and result["average_execution_time"] >= 0.0
    and result["average_qos_score"] >= 0.0
    for result in comparison.values()
)

normal_scenario_valid = (
    comparison["normal"]["completed_tasks"] == 4
    and comparison["normal"]["failed_tasks"] == 0
    and comparison["normal"]["deadline_success_rate"] == 100.0
)

tight_deadline_scenario_valid = (
    comparison["tight_deadline"]["completed_tasks"] == 3
    and comparison["tight_deadline"]["failed_tasks"] == 1
    and comparison["tight_deadline"]["deadline_success_rate"] == 75.0
)

resource_deadline_scenario_valid = (
    comparison["resource_deadline_pressure"]["completed_tasks"] == 2
    and comparison["resource_deadline_pressure"]["failed_tasks"] == 2
    and comparison[
        "resource_deadline_pressure"
    ]["deadline_success_rate"] == 50.0
)

best_qos_scenario = (
    evaluator.get_best_qos_scenario(comparison)
)

fastest_scenario = (
    evaluator.get_fastest_scenario(comparison)
)

valid_best_qos = (
    best_qos_scenario
    in comparison
)

valid_fastest = (
    fastest_scenario
    in comparison
)

if (
    all_scenarios_present
    and all_results_valid
    and normal_scenario_valid
    and tight_deadline_scenario_valid
    and resource_deadline_scenario_valid
    and valid_best_qos
    and valid_fastest
):
    print("Experiment Evaluator Test: PASSED")
else:
    print("Experiment Evaluator Test: FAILED")

print("=" * 60)