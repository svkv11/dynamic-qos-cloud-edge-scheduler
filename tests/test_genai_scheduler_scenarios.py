from genai.genai_service import GenAIService

from scheduler.compute_node import ComputeNode
from scheduler.scheduler import QoSScheduler


def create_nodes():
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


def run_scenario(service, request, task_id):
    nodes = create_nodes()
    scheduler = QoSScheduler(nodes)

    task = service.create_task(
        user_request=request,
        task_id=task_id
    )

    rankings = scheduler.get_node_rankings(task)

    best_node = scheduler.select_best_node(task)

    print()
    print("=" * 70)
    print("USER REQUEST")
    print("=" * 70)
    print(request)

    print()
    print("INTERPRETED REQUIREMENTS")
    print("-" * 70)
    print(f"Workload: {task.workload_type}")
    print(f"CPU: {task.cpu_required} cores")
    print(f"Memory: {task.memory_required_gb} GB")
    print(f"GPU: {task.gpu_required}")
    print(f"Deadline: {task.deadline_seconds} seconds")
    print(f"Priority: {task.priority}")

    print()
    print("QOS RANKINGS")
    print("-" * 70)

    for rank, item in enumerate(rankings, start=1):
        print(
            f"{rank}. {item['node'].node_id} | "
            f"Resource={item['resource_score']} | "
            f"Priority={item['priority_score']} | "
            f"Deadline={item['deadline_score']} | "
            f"Final={item['final_score']}"
        )

    print()
    print(
        f"SELECTED NODE: "
        f"{best_node.node_id if best_node else 'None'}"
    )

    if best_node is None:
        raise RuntimeError(
            "No suitable node was found."
        )

    return task, best_node


def main():
    service = GenAIService(
        use_gemini=True
    )

    scenarios = [
        {
            "name": "GPU Workload",
            "request": (
                "Run a deep learning image processing task "
                "using 8 GB memory with a GPU. "
                "Finish within 10 seconds. "
                "This is a critical priority task."
            )
        },
        {
            "name": "CPU Workload",
            "request": (
                "Run a CPU intensive computation task "
                "using 6 CPU cores and 16 GB memory. "
                "This is a high priority task."
            )
        },
        {
            "name": "Memory Workload",
            "request": (
                "Process a large dataset requiring "
                "12 GB of memory. This is a medium priority task."
            )
        },
        {
            "name": "Latency Workload",
            "request": (
                "Run a real time latency-sensitive application "
                "that must finish within 20 seconds. "
                "This is a high priority task."
            )
        }
    ]

    print()
    print("=" * 70)
    print("GENAI + DYNAMIC QOS MULTI-SCENARIO TEST")
    print("=" * 70)

    results = []

    for index, scenario in enumerate(
        scenarios,
        start=1
    ):
        task, node = run_scenario(
            service=service,
            request=scenario["request"],
            task_id=f"scenario-task-{index}"
        )

        results.append(
            {
                "scenario": scenario["name"],
                "workload": task.workload_type,
                "selected_node": node.node_id
            }
        )

    print()
    print("=" * 70)
    print("FINAL SCENARIO SUMMARY")
    print("=" * 70)

    for result in results:
        print(
            f"{result['scenario']}: "
            f"{result['workload']} -> "
            f"{result['selected_node']}"
        )

    print()
    print(
        "GenAI + Dynamic QoS Multi-Scenario Test: PASSED"
    )


if __name__ == "__main__":
    main()