from experiments.experiment_runner import ExperimentRunner


runner = ExperimentRunner()

print("=" * 60)
print("EXPERIMENT RUNNER TEST")
print("=" * 60)

print()
print("Running Standard Experiment")

result = runner.run_experiment()

print()

runner.display_result(result)

print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)

if (
    result["completed_during_cycle"] == 4
    and result["total_tasks"] == 4
    and result["completed_tasks"] == 4
    and result["failed_tasks"] == 0
    and result["deadline_success_rate"] == 100.0
    and result["average_execution_time"] > 0
    and result["average_qos_score"] > 0
    and sum(result["node_usage"].values()) == 4
):
    print("Experiment Runner Test: PASSED")
else:
    print("Experiment Runner Test: FAILED")

print("=" * 60)