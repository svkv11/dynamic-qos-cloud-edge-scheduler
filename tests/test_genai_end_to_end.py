from genai.genai_service import GenAIService

from scheduler.compute_node import ComputeNode
from scheduler.scheduler import QoSScheduler
from scheduler.task_executor import TaskExecutor
from scheduler.worker import Worker
from scheduler.worker_manager import WorkerManager
from scheduler.scheduling_controller import SchedulingController


def create_nodes():
    """
    Create the cloud and edge nodes used by the test.
    """

    return [
        ComputeNode(
            node_id="edge-01",
            node_type="edge",
            cpu_cores=4,
            memory_gb=8,
            gpu_available=False,
            cpu_utilization=25,
            memory_utilization=30,
            gpu_utilization=0,
            network_latency_ms=10
        ),

        ComputeNode(
            node_id="edge-02",
            node_type="edge",
            cpu_cores=8,
            memory_gb=16,
            gpu_available=True,
            cpu_utilization=40,
            memory_utilization=45,
            gpu_utilization=20,
            network_latency_ms=15
        ),

        ComputeNode(
            node_id="cloud-01",
            node_type="cloud",
            cpu_cores=16,
            memory_gb=32,
            gpu_available=True,
            cpu_utilization=55,
            memory_utilization=50,
            gpu_utilization=35,
            network_latency_ms=80
        )
    ]


def create_worker_manager(nodes):
    """
    Create one worker for each compute node.
    """

    workers = [
        Worker(
            worker_id="worker-edge-01",
            node=nodes[0]
        ),

        Worker(
            worker_id="worker-edge-02",
            node=nodes[1]
        ),

        Worker(
            worker_id="worker-cloud-01",
            node=nodes[2]
        )
    ]

    return WorkerManager(workers)


def main():
    print()
    print("=" * 60)
    print("GENAI END-TO-END SCHEDULING TEST")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1: User gives a natural-language request
    # --------------------------------------------------

    user_request = (
        "Generate an AI image as soon as possible."
    )

    print()
    print("USER REQUEST")
    print("-" * 60)
    print(user_request)

    # --------------------------------------------------
    # STEP 2: Gemini interprets the request
    # --------------------------------------------------

    service = GenAIService(
        use_gemini=True
    )

    task = service.create_task(
        user_request=user_request,
        task_id="genai-e2e-task-01"
    )

    print()
    print("STEP 1 - GEMINI + WORKLOAD PROFILER")
    print("-" * 60)

    print(
        f"Workload Type: "
        f"{task.workload_type}"
    )

    print(
        f"CPU Required: "
        f"{task.cpu_required} cores"
    )

    print(
        f"Memory Required: "
        f"{task.memory_required_gb} GB"
    )

    print(
        f"GPU Required: "
        f"{task.gpu_required}"
    )

    print(
        f"Deadline: "
        f"{task.deadline_seconds}"
    )

    print(
        f"Priority: "
        f"{task.priority}"
    )

    # --------------------------------------------------
    # STEP 3: Create scheduler infrastructure
    # --------------------------------------------------

    nodes = create_nodes()

    scheduler = QoSScheduler(nodes)

    executor = TaskExecutor()

    worker_manager = create_worker_manager(
        nodes
    )

    controller = SchedulingController(
        scheduler=scheduler,
        executor=executor,
        worker_manager=worker_manager
    )
    controller.start_workers()

    # --------------------------------------------------
    # STEP 4: Add the Gemini-created task
    # --------------------------------------------------

    scheduler.add_task(task)

    print()
    print("STEP 2 - TASK ADDED TO SCHEDULER")
    print("-" * 60)

    print(
        f"Pending Tasks: "
        f"{scheduler.pending_task_count()}"
    )

    # --------------------------------------------------
    # STEP 5: Run scheduling controller
    # --------------------------------------------------

    print()
    print("STEP 3 - RUNNING SCHEDULER")
    print("-" * 60)

    completed = controller.run_cycle()

    print(
        f"Completed Tasks: {completed}"
    )

    # --------------------------------------------------
    # STEP 6: Display final result
    # --------------------------------------------------

    print()
    print("STEP 4 - FINAL RESULT")
    print("-" * 60)

    print(
        f"Task State: {task.state}"
    )

    if task.assigned_node is not None:
        print(
            f"Assigned Node: "
            f"{task.assigned_node.node_id}"
        )

    print(
        f"Completed Count: "
        f"{controller.get_completed_task_count()}"
    )

    print(
        f"Failed Count: "
        f"{controller.get_failed_task_count()}"
    )

    # --------------------------------------------------
    # STEP 7: Verify
    # --------------------------------------------------

    assert task.state == "COMPLETED"

    assert task.assigned_node is not None

    assert controller.get_completed_task_count() == 1

    assert controller.get_failed_task_count() == 0

    print()
    print("=" * 60)
    print("GENAI END-TO-END TEST: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()