from compute_node import ComputeNode
from task import Task
from scheduler import QoSScheduler
from task_executor import TaskExecutor


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


# Create the infrastructure only once.
# Resource state will therefore change as tasks are scheduled.
nodes = create_nodes()

scheduler = QoSScheduler(nodes)
executor = TaskExecutor()


for task in tasks:

    print()
    print("=" * 60)
    print(f"Task Arrival: {task.task_id}")
    print(f"Workload: {task.workload_type}")
    print("=" * 60)

    print("Node State Before Scheduling:")

    for node in nodes:
        print(
            f"{node.node_id} | "
            f"CPU={node.cpu_utilization:.2f}% | "
            f"Memory={node.memory_utilization:.2f}% | "
            f"GPU={node.gpu_utilization:.2f}%"
        )

    best_node = scheduler.select_best_node(task)

    if best_node is None:
        print("No feasible node available.")
        continue

    print()
    print(f"Selected Node: {best_node.node_id}")

    allocated = best_node.allocate_task(task)

    if not allocated:
        print("Task allocation failed.")
        continue

    print()
    print("Node State After Allocation:")

    best_node.display_info()

    result = executor.execute_task(
        task,
        best_node
    )

    print(f"Execution Time: {result['execution_time']} seconds")
    print(f"Deadline: {result['deadline_seconds']} seconds")
    print(f"Deadline Met: {result['deadline_met']}")

    print()
    print("Node State After Execution:")

    best_node.display_info()