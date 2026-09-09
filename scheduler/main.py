from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
from scheduler.task_executor import TaskExecutor


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


# ---------------------------------------------------------
# Create infrastructure and scheduler
# ---------------------------------------------------------

nodes = create_nodes()

scheduler = QoSScheduler(nodes)
executor = TaskExecutor()


print("=" * 60)
print("DYNAMIC QOS CLOUD-EDGE SCHEDULER")
print("=" * 60)


# ---------------------------------------------------------
# Phase 1: Add all tasks to the scheduler queue
# ---------------------------------------------------------

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
print(f"Pending Tasks: {scheduler.pending_task_count()}")


# ---------------------------------------------------------
# Phase 2: Schedule tasks from the queue
# ---------------------------------------------------------

print()
print("=" * 60)
print("SCHEDULING TASKS FROM QUEUE")
print("=" * 60)


active_tasks = []


while scheduler.has_pending_tasks():

    task = scheduler.get_next_task()

    if task is None:
        break

    print()
    print("=" * 60)
    print(f"Scheduling Task: {task.task_id}")
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

        print()
        print("No feasible node available.")

        # Put the task back into the queue
        scheduler.task_queue.pending_tasks.insert(
            0,
            task
        )

        break

    print()
    print(f"Selected Node: {best_node.node_id}")

    allocated = best_node.allocate_task(task)

    if not allocated:

        print("Task allocation failed.")

        scheduler.task_queue.pending_tasks.insert(
            0,
            task
        )

        break

    task_state = executor.start_task(
        task,
        best_node
    )

    active_tasks.append(task_state)

    print()
    print("Task Started")
    print(f"State: {task.state}")
    print(
        f"Estimated Execution Time: "
        f"{task_state['execution_time']} seconds"
    )

    print()
    print("Node State After Allocation:")

    best_node.display_info()

    print(
        f"Remaining Pending Tasks: "
        f"{scheduler.pending_task_count()}"
    )


# ---------------------------------------------------------
# Phase 3: Complete active tasks
# ---------------------------------------------------------

print()
print("=" * 60)
print("COMPLETING ACTIVE TASKS")
print("=" * 60)


for task_state in active_tasks:

    result = executor.complete_task(
        task_state
    )

    print()
    print(f"Completed Task: {result['task_id']}")
    print(f"Node: {result['node_id']}")
    print(
        f"Execution Time: "
        f"{result['execution_time']} seconds"
    )
    print(
        f"Deadline: "
        f"{result['deadline_seconds']} seconds"
    )
    print(
        f"Deadline Met: "
        f"{result['deadline_met']}"
    )
    print(f"State: {result['state']}")


# ---------------------------------------------------------
# Phase 4: Final infrastructure state
# ---------------------------------------------------------

print()
print("=" * 60)
print("FINAL NODE STATES")
print("=" * 60)


for node in nodes:
    node.display_info()


print()
print("=" * 60)
print(
    f"Remaining Pending Tasks: "
    f"{scheduler.pending_task_count()}"
)
print("=" * 60)