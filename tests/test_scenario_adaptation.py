from experiments.experiment_runner import ExperimentRunner


runner = ExperimentRunner()

print("=" * 60)
print("SCENARIO ADAPTATION TEST")
print("=" * 60)

scenarios = [
    "normal",
    "high_cpu",
    "high_memory",
    "high_latency"
]

results = {}

for scenario in scenarios:
    print()
    print(f"Running scenario: {scenario}")

    result = runner.run_experiment(scenario)

    results[scenario] = result

    print(
        f"Completed={result['completed_tasks']} | "
        f"Failed={result['failed_tasks']} | "
        f"QoS={result['average_qos_score']} | "
        f"Execution Time={result['average_execution_time']}s"
    )


print()
print("=" * 60)
print("ADAPTATION ANALYSIS")
print("=" * 60)

normal_task_03 = results["normal"]["initial_rankings"]["task-03"]
high_cpu_task_03 = results["high_cpu"]["initial_rankings"]["task-03"]
high_memory_task_03 = results["high_memory"]["initial_rankings"]["task-03"]
high_latency_task_03 = results["high_latency"]["initial_rankings"]["task-03"]


normal_best = normal_task_03[0]["node_id"]
high_cpu_best = high_cpu_task_03[0]["node_id"]
high_memory_best = high_memory_task_03[0]["node_id"]
high_latency_best = high_latency_task_03[0]["node_id"]


print()
print(f"Normal task-03 best node: {normal_best}")
print(f"High CPU task-03 best node: {high_cpu_best}")
print(f"High Memory task-03 best node: {high_memory_best}")
print(f"High Latency task-03 best node: {high_latency_best}")


normal_test = (
    normal_best == "edge-02"
)

high_cpu_test = (
    high_cpu_best == "cloud-01"
)

high_memory_test = (
    high_memory_best == "cloud-01"
)

high_latency_test = (
    high_latency_best == "cloud-01"
)


all_tasks_completed = all(
    result["completed_tasks"] == 4
    and result["failed_tasks"] == 0
    and result["deadline_success_rate"] == 100.0
    for result in results.values()
)


print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)

print(
    f"Normal adaptation test: "
    f"{'PASSED' if normal_test else 'FAILED'}"
)

print(
    f"High CPU adaptation test: "
    f"{'PASSED' if high_cpu_test else 'FAILED'}"
)

print(
    f"High Memory adaptation test: "
    f"{'PASSED' if high_memory_test else 'FAILED'}"
)

print(
    f"High Latency adaptation test: "
    f"{'PASSED' if high_latency_test else 'FAILED'}"
)

print(
    f"Task completion test: "
    f"{'PASSED' if all_tasks_completed else 'FAILED'}"
)


if (
    normal_test
    and high_cpu_test
    and high_memory_test
    and high_latency_test
    and all_tasks_completed
):
    print()
    print("Scenario Adaptation Test: PASSED")
else:
    print()
    print("Scenario Adaptation Test: FAILED")

print("=" * 60)