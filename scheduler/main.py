from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
from scheduler.task_executor import TaskExecutor
from scheduler.worker import Worker


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
# Create infrastructure, scheduler, executor and workers
# ---------------------------------------------------------

nodes = create_nodes()

scheduler = QoSScheduler(nodes)
executor = TaskExecutor()

workers = [
    Worker("worker-01", nodes[0]),
    Worker("worker-02", nodes[1]),
    Worker("worker-03", nodes[2])
]

for worker in workers:
    worker.start()


# ---------------------------------------------------------
# Create node-to-worker mapping
# ---------------------------------------------------------

worker_map = {
    worker.node.node_id: worker
    for worker in workers
}


def get_available_nodes():
    """
    Return nodes whose workers are currently READY.
    """

    return [
        worker.node
        for worker in workers
        if worker.status == "READY"
    ]


print("=" * 60)
print("DYNAMIC QOS CLOUD-EDGE SCHEDULER")
print("=" * 60)


# ---------------------------------------------------------
# Display worker information
# ---------------------------------------------------------

print()
print("=" * 60)
print("WORKER STATUS")
print("=" * 60)

for worker in workers:
    worker.display_info()


# ---------------------------------------------------------
# Phase 1: Add tasks to the QoS-aware queue
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
# Phase 2: Schedule tasks from queue
# ---------------------------------------------------------

print()
print("=" * 60)
print("SCHEDULING TASKS FROM QUEUE")
print("=" * 60)


active_tasks = []


while scheduler.has_pending_tasks():

    available_nodes = get_available_nodes()

    result = scheduler.schedule_next_task(
        available_nodes
    )

    if result is None:

        print()
        print("No READY worker with a feasible node is available.")

        print(
            f"Pending Tasks Waiting: "
            f"{scheduler.pending_task_count()}"
        )

        break

    task, best_node = result

    worker = worker_map[best_node.node_id]

    task_state = worker.execute_task(
        task,
        executor
    )

    if task_state is None:

        print()
        print(
            f"Worker {worker.worker_id} "
            f"is not available."
        )

        break

    active_tasks.append(
        {
            "task_state": task_state,
            "worker": worker
        }
    )

    print()
    print("=" * 60)
    print(f"Task Started: {task.task_id}")
    print(f"Workload: {task.workload_type}")
    print(f"Selected Node: {best_node.node_id}")
    print(f"Worker: {worker.worker_id}")
    print(f"Worker Status: {worker.status}")
    print(f"Priority: {task.priority}")
    print(f"Deadline: {task.deadline_seconds}s")
    print(f"State: {task.state}")

    print(
        f"Estimated Execution Time: "
        f"{task_state['execution_time']} seconds"
    )

    print("=" * 60)

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


completed_count = 0


while active_tasks:

    active_task = active_tasks.pop(0)

    task_state = active_task["task_state"]
    worker = active_task["worker"]

    result = executor.complete_task(
        task_state
    )

    worker.task_finished()

    completed_count += 1

    print()
    print(f"Completed Task: {result['task_id']}")
    print(f"Node: {result['node_id']}")
    print(f"Worker: {worker.worker_id}")
    print(f"Worker Status: {worker.status}")

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

    # -----------------------------------------------------
    # Retry pending tasks after a worker becomes READY
    # -----------------------------------------------------

    if scheduler.has_pending_tasks():

        print()
        print("-" * 60)
        print("RETRYING PENDING TASKS AFTER WORKER BECOMES READY")
        print("-" * 60)

        available_nodes = get_available_nodes()

        retry_results = scheduler.retry_pending_tasks(
            available_nodes
        )

        for retry_task, retry_node in retry_results:

            retry_worker = worker_map[
                retry_node.node_id
            ]

            retry_state = retry_worker.execute_task(
                retry_task,
                executor
            )

            if retry_state is None:

                print(
                    f"Worker {retry_worker.worker_id} "
                    f"is not available."
                )

                continue

            active_tasks.append(
                {
                    "task_state": retry_state,
                    "worker": retry_worker
                }
            )

            print(
                f"Retried Task: {retry_task.task_id} | "
                f"Selected Node: {retry_node.node_id} | "
                f"Worker: {retry_worker.worker_id} | "
                f"State: {retry_task.state}"
            )

            print(
                f"Worker Status: "
                f"{retry_worker.status}"
            )

            print(
                f"Estimated Execution Time: "
                f"{retry_state['execution_time']} seconds"
            )

        print(
            f"Pending Tasks After Retry: "
            f"{scheduler.pending_task_count()}"
        )


# ---------------------------------------------------------
# Phase 4: Final worker states
# ---------------------------------------------------------

print()
print("=" * 60)
print("FINAL WORKER STATES")
print("=" * 60)


for worker in workers:
    worker.display_info()


# ---------------------------------------------------------
# Phase 5: Final infrastructure state
# ---------------------------------------------------------

print()
print("=" * 60)
print("FINAL NODE STATES")
print("=" * 60)


for node in nodes:
    node.display_info()


print()
print("=" * 60)
print(f"Completed Tasks: {completed_count}")

print(
    f"Remaining Pending Tasks: "
    f"{scheduler.pending_task_count()}"
)

print("=" * 60)