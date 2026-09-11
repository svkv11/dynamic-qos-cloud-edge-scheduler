from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
from scheduler.task_executor import TaskExecutor
from scheduler.worker import Worker
from scheduler.worker_manager import WorkerManager
from scheduler.scheduling_controller import SchedulingController
from scheduler.resource_monitor import ResourceMonitor


def create_nodes():
    """
    Create the initial set of compute nodes.
    """

    return [
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


def create_tasks():
    """
    Create the initial workload set.
    """

    return [
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


def display_rankings(scheduler, task, title):
    """
    Display QoS rankings for a task.
    """

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    rankings = scheduler.get_node_rankings(task)

    if not rankings:
        print("No feasible nodes available.")
        return None

    for ranking in rankings:
        print(
            f"{ranking['node'].node_id} | "
            f"Resource={ranking['resource_score']} | "
            f"Priority={ranking['priority_score']} | "
            f"Deadline={ranking['deadline_score']} | "
            f"Final={ranking['final_score']}"
        )

    return rankings[0]["node"]


nodes = create_nodes()

scheduler = QoSScheduler(nodes)
executor = TaskExecutor()
resource_monitor = ResourceMonitor(nodes)

workers = [
    Worker("worker-01", nodes[0]),
    Worker("worker-02", nodes[1]),
    Worker("worker-03", nodes[2])
]

worker_manager = WorkerManager(workers)

controller = SchedulingController(
    scheduler=scheduler,
    executor=executor,
    worker_manager=worker_manager,
    resource_monitor=resource_monitor
)

controller.start_workers()

print("=" * 60)
print("DYNAMIC QOS CLOUD-EDGE SCHEDULER")
print("=" * 60)

print()
print("=" * 60)
print("INITIAL RESOURCE MONITOR STATE")
print("=" * 60)

resource_monitor.display_status()

tasks = create_tasks()

dynamic_task = tasks[0]

initial_best_node = display_rankings(
    scheduler,
    dynamic_task,
    "INITIAL QOS RANKINGS"
)

print()
print(
    f"Initial Best Node for {dynamic_task.task_id}: "
    f"{initial_best_node.node_id}"
)

print()
print("=" * 60)
print("SIMULATING RESOURCE CONDITION CHANGE")
print("=" * 60)

print("Updating edge-02 with higher resource utilization...")

resource_monitor.refresh_node_state(
    node_id="edge-02",
    cpu_utilization=85.0,
    memory_utilization=80.0,
    gpu_utilization=70.0,
    network_latency_ms=50.0
)

resource_monitor.display_status()

updated_best_node = display_rankings(
    scheduler,
    dynamic_task,
    "UPDATED QOS RANKINGS"
)

print()

if updated_best_node is not None:
    print(
        f"Updated Best Node for {dynamic_task.task_id}: "
        f"{updated_best_node.node_id}"
    )

print()
print("=" * 60)
print("DYNAMIC ADAPTATION RESULT")
print("=" * 60)

if (
    initial_best_node is not None
    and updated_best_node is not None
    and initial_best_node.node_id != updated_best_node.node_id
):
    print("Scheduler adapted to the changed resource conditions.")
    print(
        f"Before: {initial_best_node.node_id}"
    )
    print(
        f"After:  {updated_best_node.node_id}"
    )
else:
    print("Scheduler did not change its selected node.")

print()
print("=" * 60)
print("ADDING TASKS TO QUEUE")
print("=" * 60)

for task in tasks:
    added = scheduler.add_task(task)

    print(
        f"{task.task_id} | "
        f"Priority={task.priority} | "
        f"Deadline={task.deadline_seconds}s | "
        f"Added={added}"
    )

print()
print(
    f"Pending Tasks: "
    f"{scheduler.pending_task_count()}"
)

print()
print("=" * 60)
print("RUNNING SCHEDULING CYCLE")
print("=" * 60)

completed_count = controller.run_cycle()

print()
print("=" * 60)
print("FINAL CONTROLLER STATUS")
print("=" * 60)

controller.display_status()

print()
print("=" * 60)
print("FINAL WORKER STATES")
print("=" * 60)

worker_manager.display_status()

print()
print("=" * 60)
print("FINAL RESOURCE MONITOR STATE")
print("=" * 60)

resource_monitor.display_status()

print()
print("=" * 60)
print("FINAL RESULT")
print("=" * 60)

print(
    f"Completed Tasks: "
    f"{controller.get_completed_task_count()}"
)

print(
    f"Failed Tasks: "
    f"{controller.get_failed_task_count()}"
)

print(
    f"Active Tasks: "
    f"{controller.get_active_task_count()}"
)

print(
    f"Remaining Pending Tasks: "
    f"{scheduler.pending_task_count()}"
)

print(
    f"Scheduling Cycle Completed: "
    f"{completed_count}"
)

print("=" * 60)