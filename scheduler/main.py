from compute_node import ComputeNode
from task import Task
from scheduler import QoSScheduler


edge_1 = ComputeNode(
    node_id="edge-01",
    node_type="edge",
    cpu_cores=4,
    memory_gb=8,
    gpu_available=False,
    cpu_utilization=25.0,
    memory_utilization=30.0,
    gpu_utilization=0.0,
    network_latency_ms=10.0
)


edge_2 = ComputeNode(
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


cloud_1 = ComputeNode(
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


image_task = Task(
    task_id="task-001",
    workload_type="image_processing",
    cpu_required=2,
    memory_required_gb=2,
    gpu_required=False,
    deadline_seconds=5,
    priority=2
)


video_task = Task(
    task_id="task-002",
    workload_type="video_processing",
    cpu_required=4,
    memory_required_gb=8,
    gpu_required=True,
    deadline_seconds=10,
    priority=1
)


nodes = [
    edge_1,
    edge_2,
    cloud_1
]


scheduler = QoSScheduler(nodes)


print("Task-001 Best Node:")

best_node = scheduler.select_best_node(image_task)

if best_node:
    print(best_node.node_id)
else:
    print("No suitable node found")


print()

print("Task-002 Best Node:")

best_node = scheduler.select_best_node(video_task)

if best_node:
    print(best_node.node_id)
else:
    print("No suitable node found")