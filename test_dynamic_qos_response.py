from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
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
    ),

    ComputeNode(
        node_id="cloud-01",
        node_type="cloud",
        cpu_cores=16,
        memory_gb=32,
        gpu_available=True,
        cpu_utilization=55.0,
        memory_utilization=50.0,
        gpu_utilization=35.0,
        network_latency_ms=80.0
    )
]


scheduler = QoSScheduler(nodes)
monitor = ResourceMonitor(nodes)


task = Task(
    task_id="dynamic-test",
    workload_type="cpu_intensive",
    cpu_required=3,
    memory_required_gb=2,
    gpu_required=False,
    deadline_seconds=60,
    priority=2
)


print("=" * 60)
print("DYNAMIC QOS RESPONSE TEST")
print("=" * 60)


# ---------------------------------------------------------
# Initial scheduling decision
# ---------------------------------------------------------

print()
print("INITIAL NODE CONDITIONS")

monitor.display_status()


initial_rankings = scheduler.get_node_rankings(task)

print()
print("INITIAL NODE RANKINGS")

for ranking in initial_rankings:
    print(
        f"{ranking['node'].node_id} | "
        f"Resource={ranking['resource_score']} | "
        f"Final={ranking['final_score']}"
    )


initial_best_node = scheduler.select_best_node(task)

print()
print(
    f"Initial Best Node: "
    f"{initial_best_node.node_id}"
)


# ---------------------------------------------------------
# Change edge-02 resource conditions
# ---------------------------------------------------------

print()
print("UPDATING EDGE-02 RESOURCE CONDITIONS")

monitor.update_node_state(
    node_id="edge-02",
    cpu_utilization=85.0,
    memory_utilization=80.0,
    gpu_utilization=70.0,
    network_latency_ms=50.0
)

monitor.display_status()


# ---------------------------------------------------------
# Recalculate scheduling decision
# ---------------------------------------------------------

print()
print("UPDATED NODE RANKINGS")

updated_rankings = scheduler.get_node_rankings(task)

for ranking in updated_rankings:
    print(
        f"{ranking['node'].node_id} | "
        f"Resource={ranking['resource_score']} | "
        f"Final={ranking['final_score']}"
    )


updated_best_node = scheduler.select_best_node(task)

print()
print(
    f"Updated Best Node: "
    f"{updated_best_node.node_id}"
)


# ---------------------------------------------------------
# Check whether edge-02 became infeasible
# ---------------------------------------------------------

edge_02_initially_available = any(
    ranking["node"].node_id == "edge-02"
    for ranking in initial_rankings
)

edge_02_available_after_update = any(
    ranking["node"].node_id == "edge-02"
    for ranking in updated_rankings
)


# ---------------------------------------------------------
# Verify dynamic behavior
# ---------------------------------------------------------

print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)


if (
    initial_best_node.node_id == "edge-02"
    and updated_best_node.node_id == "edge-01"
    and edge_02_initially_available
    and not edge_02_available_after_update
):
    print("Dynamic QoS Response Test: PASSED")
else:
    print("Dynamic QoS Response Test: FAILED")


print("=" * 60)