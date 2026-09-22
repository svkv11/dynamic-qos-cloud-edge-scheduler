from genai.genai_service import GenAIService

from scheduler.compute_node import ComputeNode
from scheduler.scheduler import QoSScheduler

from execution.workload_runner import WorkloadRunner


def create_nodes():
    """
    Create the cloud and edge nodes used by the live demo.
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


def display_rankings(rankings):
    """
    Display the QoS ranking of feasible nodes.
    """

    print()
    print("=" * 60)
    print("QOS NODE RANKINGS")
    print("=" * 60)

    if not rankings:
        print("No suitable node is available.")
        return

    for rank, item in enumerate(rankings, start=1):
        node = item["node"]

        print(f"{rank}. {node.node_id}")
        print(f"   Type: {node.node_type}")
        print(
            f"   Resource Score: "
            f"{item['resource_score']}"
        )
        print(
            f"   Priority Score: "
            f"{item['priority_score']}"
        )
        print(
            f"   Deadline Score: "
            f"{item['deadline_score']}"
        )
        print(
            f"   Final QoS Score: "
            f"{item['final_score']}"
        )
        print("-" * 60)


def main():
    print()
    print("=" * 60)
    print("GENAI + DYNAMIC QOS + LIVE EXECUTION")
    print("=" * 60)

    print()
    print(
        "Enter a natural-language task requirement."
    )

    print(
        "Example:"
    )

    print(
        "Run a CPU intensive task using 2 CPU cores "
        "and 2 GB memory within 10 seconds."
    )

    print()

    user_request = input(
        "Enter your task: "
    ).strip()

    if not user_request:
        print()
        print("No task request was entered.")
        return

    # --------------------------------------------------
    # Step 1: Local GenAI requirement interpretation
    # --------------------------------------------------

    print()
    print(
        "Interpreting task requirements using "
        "Ollama + Qwen3:4b-instruct..."
    )

    service = GenAIService(
        use_ollama=True
    )

    try:
        task = service.create_task(
            user_request=user_request,
            task_id="live-execution-task-01"
        )

    except Exception as error:
        print()
        print("Failed to interpret task.")
        print(f"Error: {error}")
        return

    # --------------------------------------------------
    # Step 2: Display interpreted requirements
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("INTERPRETED REQUIREMENTS")
    print("=" * 60)

    print(
        f"Workload Type: {task.workload_type}"
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
        f"{task.deadline_seconds} seconds"
    )

    print(
        f"Priority: {task.priority}"
    )

    # --------------------------------------------------
    # Step 3: Create nodes and scheduler
    # --------------------------------------------------

    nodes = create_nodes()

    scheduler = QoSScheduler(nodes)

    # --------------------------------------------------
    # Step 4: Calculate QoS rankings
    # --------------------------------------------------

    rankings = scheduler.get_node_rankings(
        task
    )

    display_rankings(rankings)

    # --------------------------------------------------
    # Step 5: Select best node
    # --------------------------------------------------

    best_node = scheduler.select_best_node(
        task
    )

    print()
    print("=" * 60)
    print("SCHEDULING DECISION")
    print("=" * 60)

    if best_node is None:
        print(
            "No suitable cloud or edge node "
            "can execute this task."
        )
        return

    selected_score = rankings[0]["final_score"]

    print(
        f"Selected Node: {best_node.node_id}"
    )

    print(
        f"Node Type: {best_node.node_type}"
    )

    print(
        f"Final QoS Score: {selected_score}"
    )

    # --------------------------------------------------
    # Step 6: Allocate task
    # --------------------------------------------------

    allocated = best_node.allocate_task(
        task
    )

    if not allocated:
        print()
        print("Task allocation failed.")
        return

    task.start(best_node)

    # --------------------------------------------------
    # Step 7: Real workload execution
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("LIVE WORKLOAD EXECUTION")
    print("=" * 60)

    print(
        "Executing the workload on the selected node..."
    )

    runner = WorkloadRunner()

    result = runner.run(
        task=task,
        node=best_node
    )

    # --------------------------------------------------
    # Step 8: Display real execution result
    # --------------------------------------------------

    result.display()

    # --------------------------------------------------
    # Step 9: Release logical node resources
    # --------------------------------------------------

    best_node.release_task(task)

    print()
    print("=" * 60)
    print("LIVE DEMO COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()