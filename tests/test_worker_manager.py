from scheduler.compute_node import ComputeNode
from scheduler.worker import Worker
from scheduler.worker_manager import WorkerManager


node_01 = ComputeNode(
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

node_02 = ComputeNode(
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


worker_01 = Worker("worker-01", node_01)
worker_02 = Worker("worker-02", node_02)


manager = WorkerManager(
    [
        worker_01,
        worker_02
    ]
)


print("Initial Status")
manager.display_status()


print()
print("Starting All Workers")
manager.start_all()
manager.display_status()


print()
print("Testing Worker Lookup")

worker = manager.get_worker_for_node("edge-02")

if worker is not None:
    print(
        f"Worker for edge-02: "
        f"{worker.worker_id}"
    )
else:
    print("Worker not found")


print()
print("Testing Available Nodes")

for node in manager.get_available_nodes():
    print(
        f"Available Node: "
        f"{node.node_id}"
    )


print()
print("Stopping All Workers")
manager.stop_all()
manager.display_status()