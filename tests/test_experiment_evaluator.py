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

all_scenarios_present = (
    set(comparison.keys())
    == {
        "normal",
        "high_cpu",
        "high_memory",
        "high_latency"
    }
)

all_tasks_completed = all(
    result["completed_tasks"] == 4
    and result["failed_tasks"] == 0
    for result in comparison.values()
)

all_deadlines_met = all(
    result["deadline_success_rate"] == 100.0
    for result in comparison.values()
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
    and all_tasks_completed
    and all_deadlines_met
    and valid_best_qos
    and valid_fastest
):
    print("Experiment Evaluator Test: PASSED")
else:
    print("Experiment Evaluator Test: FAILED")

print("=" * 60)