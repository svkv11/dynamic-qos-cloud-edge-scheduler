from scheduler.compute_node import ComputeNode
from scheduler.scheduler import QoSScheduler
from scheduler.task_executor import TaskExecutor
from scheduler.worker import Worker
from scheduler.worker_manager import WorkerManager
from scheduler.scheduling_controller import SchedulingController
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


scheduler = QoSScheduler(nodes)
executor = TaskExecutor()


workers = [
    Worker("worker-01", nodes[0]),
    Worker("worker-02", nodes[1])
]


worker_manager = WorkerManager(workers)


resource_monitor = ResourceMonitor(nodes)


controller = SchedulingController(
    scheduler=scheduler,
    executor=executor,
    worker_manager=worker_manager,
    resource_monitor=resource_monitor
)


print("=" * 60)
print("RESOURCE MONITOR + CONTROLLER TEST")
print("=" * 60)


print()
print("Initial Resource State")

initial_states = controller.get_current_node_states()

for state in initial_states:
    print(state)


print()
print("Updating edge-02 Through ResourceMonitor")

updated = resource_monitor.update_node_state(
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
print("Resource State Through Controller")

updated_states = controller.get_current_node_states()

for state in updated_states:
    print(state)


print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)


edge_02_state = None

for state in updated_states:
    if state["node_id"] == "edge-02":
        edge_02_state = state


if (
    updated
    and edge_02_state is not None
    and edge_02_state["cpu_utilization"] == 75.0
    and edge_02_state["memory_utilization"] == 60.0
    and edge_02_state["gpu_utilization"] == 50.0
    and edge_02_state["network_latency_ms"] == 30.0
):
    print("Resource Monitor Controller Test: PASSED")
else:
    print("Resource Monitor Controller Test: FAILED")


print("=" * 60)