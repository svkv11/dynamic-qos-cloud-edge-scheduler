from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
from scheduler.task_executor import TaskExecutor
from scheduler.worker import Worker
from scheduler.worker_manager import WorkerManager
from scheduler.scheduling_controller import SchedulingController


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


tasks = [
    Task(
        task_id="task-cpu",
        workload_type="cpu_intensive",
        cpu_required=3,
        memory_required_gb=2,
        gpu_required=False,
        deadline_seconds=60,
        priority=2
    ),

    Task(
        task_id="task-memory",
        workload_type="memory_intensive",
        cpu_required=2,
        memory_required_gb=6,
        gpu_required=False,
        deadline_seconds=60,
        priority=2
    ),

    Task(
        task_id="task-gpu",
        workload_type="gpu_intensive",
        cpu_required=4,
        memory_required_gb=8,
        gpu_required=True,
        deadline_seconds=30,
        priority=3
    ),

    Task(
        task_id="task-latency",
        workload_type="latency_sensitive",
        cpu_required=1,
        memory_required_gb=1,
        gpu_required=False,
        deadline_seconds=5,
        priority=5
    )
]


scheduler = QoSScheduler(nodes)
executor = TaskExecutor()


workers = [
    Worker("worker-01", nodes[0]),
    Worker("worker-02", nodes[1]),
    Worker("worker-03", nodes[2])
]


worker_manager = WorkerManager(workers)


controller = SchedulingController(
    scheduler=scheduler,
    executor=executor,
    worker_manager=worker_manager
)


for task in tasks:
    scheduler.add_task(task)


print("=" * 60)
print("SCHEDULING CONTROLLER TEST")
print("=" * 60)


print()
print("Starting Workers")

controller.start_workers()

worker_manager.display_status()


print()
print("Initial Controller Status")

controller.display_status()


print()
print("Running Scheduling Cycle")

completed = controller.run_cycle()


print()
print("Final Controller Status")

controller.display_status()


print()
print(
    f"Completed During Cycle: "
    f"{completed}"
)


print()
print("Final Worker Status")

worker_manager.display_status()


print()
print("Final Node States")

for node in nodes:
    node.display_info()


print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)

if (
    controller.get_completed_task_count() == 4
    and controller.get_active_task_count() == 0
    and scheduler.pending_task_count() == 0
):
    print("Scheduling Controller Test: PASSED")
else:
    print("Scheduling Controller Test: FAILED")

print("=" * 60)