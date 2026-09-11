from experiments.experiment_scenarios import ExperimentScenarios


print("=" * 60)
print("EXPERIMENT SCENARIOS TEST")
print("=" * 60)

scenarios = {
    "normal": ExperimentScenarios.normal(),
    "high_cpu": ExperimentScenarios.high_cpu(),
    "high_memory": ExperimentScenarios.high_memory(),
    "high_latency": ExperimentScenarios.high_latency()
}

for name, conditions in scenarios.items():

    print()
    print(f"{name.upper()} SCENARIO")
    print("-" * 60)

    for node_id, state in conditions.items():
        print(
            f"{node_id} | "
            f"CPU={state['cpu_utilization']}% | "
            f"Memory={state['memory_utilization']}% | "
            f"GPU={state['gpu_utilization']}% | "
            f"Latency={state['network_latency_ms']} ms"
        )


normal = scenarios["normal"]
high_cpu = scenarios["high_cpu"]
high_memory = scenarios["high_memory"]
high_latency = scenarios["high_latency"]


print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)

cpu_test = (
    normal["edge-02"]["cpu_utilization"] == 40.0
    and high_cpu["edge-02"]["cpu_utilization"] == 85.0
)

memory_test = (
    normal["edge-02"]["memory_utilization"] == 45.0
    and high_memory["edge-02"]["memory_utilization"] == 80.0
)

latency_test = (
    normal["edge-02"]["network_latency_ms"] == 15.0
    and high_latency["edge-02"]["network_latency_ms"] == 50.0
)

unchanged_test = (
    high_cpu["edge-02"]["memory_utilization"] == 45.0
    and high_memory["edge-02"]["cpu_utilization"] == 40.0
    and high_latency["edge-02"]["cpu_utilization"] == 40.0
    and high_latency["edge-02"]["memory_utilization"] == 45.0
)

if (
    cpu_test
    and memory_test
    and latency_test
    and unchanged_test
):
    print("Experiment Scenarios Test: PASSED")
else:
    print("Experiment Scenarios Test: FAILED")

print("=" * 60)