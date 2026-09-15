from scheduler.compute_node import ComputeNode
from scheduler.scheduler import QoSScheduler

from genai.mock_interpreter import MockRequirementInterpreter
from genai.task_converter import TaskConverter


def main():
    print("=" * 70)
    print("GENAI END-TO-END PIPELINE TEST")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Natural-language user request
    # ---------------------------------------------------------

    user_request = (
        "Run a GPU image processing task "
        "using 8 GB memory and finish "
        "within 10 seconds. "
        "This is a critical priority task."
    )

    print("USER REQUEST")
    print("-" * 70)
    print(user_request)
    print()

    # ---------------------------------------------------------
    # 2. Interpret natural language
    # ---------------------------------------------------------

    interpreter = MockRequirementInterpreter()

    requirements = interpreter.interpret(
        user_request
    )

    print("INTERPRETED REQUIREMENTS")
    print("-" * 70)

    requirements.display_info()
    print()

    # ---------------------------------------------------------
    # 3. Convert requirements into existing Task model
    # ---------------------------------------------------------

    task = TaskConverter.requirements_to_task(
        requirements=requirements,
        task_id="genai-task-01"
    )

    print("GENERATED TASK")
    print("-" * 70)

    task.display_info()
    print()

    # ---------------------------------------------------------
    # 4. Create scheduler nodes
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # 5. Run the existing Dynamic QoS Scheduler
    # ---------------------------------------------------------

    scheduler = QoSScheduler(nodes)

    rankings = scheduler.get_node_rankings(task)

    print("QOS NODE RANKINGS")
    print("-" * 70)

    for index, ranking in enumerate(
        rankings,
        start=1
    ):
        print(
            f"{index}. "
            f"{ranking['node'].node_id} | "
            f"Resource={ranking['resource_score']} | "
            f"Priority={ranking['priority_score']} | "
            f"Deadline={ranking['deadline_score']} | "
            f"Final={ranking['final_score']}"
        )

    print()

    # ---------------------------------------------------------
    # 6. Select the best node
    # ---------------------------------------------------------

    selected_node = scheduler.select_best_node(
        task
    )

    print("SCHEDULER DECISION")
    print("-" * 70)

    if selected_node is not None:
        print(
            f"Selected Node: "
            f"{selected_node.node_id}"
        )
    else:
        print("Selected Node: None")

    # ---------------------------------------------------------
    # 7. Validate complete pipeline
    # ---------------------------------------------------------

    assert task.task_id == "genai-task-01"
    assert task.workload_type == "gpu_intensive"
    assert task.cpu_required == 4
    assert task.memory_required_gb == 8
    assert task.gpu_required is True
    assert task.deadline_seconds == 10
    assert task.priority == 5

    assert selected_node is not None
    assert selected_node.gpu_available is True

    print()
    print("=" * 70)
    print("TEST RESULT")
    print("=" * 70)
    print("GenAI End-to-End Pipeline Test: PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()