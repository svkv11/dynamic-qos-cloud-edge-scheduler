from scheduler.compute_node import ComputeNode
from scheduler.resource_monitor import ResourceMonitor


nodes = [
    ComputeNode(
        node_id="edge-01",
        node_type="edge",
        cpu_cores=4,
        memory_gb=8,
        gpu_available=False,
        cpu_utilization=25.0,
        memory_utilization=30.0,
        gpu_utilization=0.0,
        network_latency_ms=10.0
    ),

    ComputeNode(
        node_id="edge-02",
        node_type="edge",
        cpu_cores=8,
        memory_gb=16,
        gpu_available=True,
        cpu_utilization=40.0,
        memory_utilization=45.0,
        gpu_utilization=20.0,
        network_latency_ms=15.0
    )
]


monitor = ResourceMonitor(nodes)


print("=" * 60)
print("RESOURCE MONITOR TEST")
print("=" * 60)


print()
print("Initial Node States")

monitor.display_status()


print()
print("Updating edge-02 Resource State")

updated = monitor.update_node_state(
    node_id="edge-02",
    cpu_utilization=75.0,
    memory_utilization=60.0,
    gpu_utilization=50.0,
    network_latency_ms=30.0
)

print(
    f"Update Successful: {updated}"
)


print()
print("Updated Node States")

monitor.display_status()


print()
print("Checking Individual Node State")

state = monitor.get_node_state("edge-02")

print(state)


print()
print("Checking All Node States")

all_states = monitor.get_all_node_states()

for node_state in all_states:
    print(node_state)


print()
print("Checking Invalid Node")

invalid_state = monitor.get_node_state("unknown-node")

print(
    f"Unknown Node State: {invalid_state}"
)


print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)


if (
    updated
    and state["cpu_utilization"] == 75.0
    and state["memory_utilization"] == 60.0
    and state["gpu_utilization"] == 50.0
    and state["network_latency_ms"] == 30.0
    and invalid_state is None
):
    print("Resource Monitor Test: PASSED")
else:
    print("Resource Monitor Test: FAILED")


print("=" * 60)