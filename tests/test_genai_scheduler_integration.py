from genai.genai_service import GenAIService

from scheduler.compute_node import ComputeNode
from scheduler.scheduler import QoSScheduler


def create_nodes():
    """
    Create the same sample edge/cloud nodes
    used by the existing scheduler tests.
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


def main():
    print()
    print("=" * 60)
    print("GENAI + DYNAMIC QOS SCHEDULER INTEGRATION TEST")
    print("=" * 60)

    # --------------------------------------------------
    # Step 1: Natural-language user request
    # --------------------------------------------------

    user_request = (
        "Run a GPU image processing task using "
        "8 GB memory and finish within 10 seconds. "
        "This is a critical priority task."
    )

    print()
    print("USER REQUEST:")
    print(user_request)

    # --------------------------------------------------
    # Step 2: Gemini interprets the request
    # --------------------------------------------------

    genai_service = GenAIService(
        use_gemini=True
    )

    task = genai_service.create_task(
        user_request=user_request,
        task_id="integration-task-01"
    )

    print()
    print("=" * 60)
    print("STEP 1 - GEMINI CREATED TASK")
    print("=" * 60)

    task.display_info()

    # --------------------------------------------------
    # Step 3: Create scheduler and nodes
    # --------------------------------------------------

    nodes = create_nodes()

    scheduler = QoSScheduler(nodes)

    # --------------------------------------------------
    # Step 4: Get QoS rankings
    # --------------------------------------------------

    rankings = scheduler.get_node_rankings(task)

    print()
    print("=" * 60)
    print("STEP 2 - DYNAMIC QOS NODE RANKINGS")
    print("=" * 60)

    for rank, item in enumerate(rankings, start=1):
        print(
            f"{rank}. {item['node'].node_id} "
            f"| Resource: {item['resource_score']} "
            f"| Priority: {item['priority_score']} "
            f"| Deadline: {item['deadline_score']} "
            f"| Final: {item['final_score']}"
        )

    # --------------------------------------------------
    # Step 5: Select the best node
    # --------------------------------------------------

    best_node = scheduler.select_best_node(task)

    print()
    print("=" * 60)
    print("STEP 3 - SELECTED NODE")
    print("=" * 60)

    if best_node is None:
        print("No suitable node found.")
        raise RuntimeError(
            "Dynamic QoS Scheduler could not schedule the task."
        )

    print(
        f"Selected Node: {best_node.node_id}"
    )

    print(
        f"Node Type: {best_node.node_type}"
    )

    # --------------------------------------------------
    # Step 6: Allocate the task
    # --------------------------------------------------

    allocated = best_node.allocate_task(task)

    if not allocated:
        raise RuntimeError(
            "Task allocation failed."
        )

    task.start(best_node)

    print()
    print("=" * 60)
    print("STEP 4 - TASK SCHEDULED")
    print("=" * 60)

    task.display_info()

    # --------------------------------------------------
    # Final validation
    # --------------------------------------------------

    assert task.workload_type == "gpu_intensive"
    assert task.cpu_required == 4
    assert task.memory_required_gb == 8
    assert task.gpu_required is True
    assert task.deadline_seconds == 10
    assert task.priority == 5
    assert task.assigned_node is best_node
    assert best_node.gpu_available is True

    print(
        "GenAI + Dynamic QoS Scheduler "
        "Integration Test: PASSED"
    )


if __name__ == "__main__":
    main()