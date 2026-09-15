import os
import sys


# Add the project root directory to Python's import path.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from llm_requirement_interpreter import (
    LLMRequirementInterpreter
)

from workload_profiler import (
    WorkloadProfiler
)

from scheduler.task import Task

from scheduler.scheduler import (
    QoSScheduler
)

from scheduler.compute_node import (
    ComputeNode
)


print("=" * 60)
print("LLM + PROFILER + TASK + QOS SCHEDULER TEST")
print("=" * 60)


# ------------------------------------------------------
# Step 1: Create the available compute nodes
# ------------------------------------------------------

nodes = [
    ComputeNode(
        node_id="edge-01",
        node_type="edge",
        cpu_cores=4,
        memory_gb=8,
        gpu_available=False
    ),
    ComputeNode(
        node_id="edge-02",
        node_type="edge",
        cpu_cores=8,
        memory_gb=16,
        gpu_available=True
    ),
    ComputeNode(
        node_id="cloud-01",
        node_type="cloud",
        cpu_cores=16,
        memory_gb=32,
        gpu_available=True
    )
]


# ------------------------------------------------------
# Step 2: Set current node states
# ------------------------------------------------------

nodes[0].cpu_utilization = 25
nodes[0].memory_utilization = 30
nodes[0].gpu_utilization = 0
nodes[0].network_latency_ms = 10

nodes[1].cpu_utilization = 40
nodes[1].memory_utilization = 45
nodes[1].gpu_utilization = 20
nodes[1].network_latency_ms = 15

nodes[2].cpu_utilization = 55
nodes[2].memory_utilization = 50
nodes[2].gpu_utilization = 35
nodes[2].network_latency_ms = 80


# ------------------------------------------------------
# Step 3: User request
# ------------------------------------------------------

user_request = "Create an AI image quickly."


print("\nUser Request:")
print(user_request)


try:

    # --------------------------------------------------
    # Step 4: Interpret user request using Qwen
    # --------------------------------------------------

    interpreted_requirements = (
        LLMRequirementInterpreter.interpret(
            user_request
        )
    )

    print("\nLLM Interpretation:")
    print(interpreted_requirements)


    # --------------------------------------------------
    # Step 5: Convert interpretation into
    #         technical requirements
    # --------------------------------------------------

    final_requirements = (
        WorkloadProfiler.build_requirements(
            interpreted_requirements
        )
    )

    print("\nFinal Profiled Requirements:")
    print(final_requirements)


    # --------------------------------------------------
    # Step 6: Create Task
    # --------------------------------------------------

    task = Task(
        task_id="llm-task-001",
        workload_type=final_requirements["workload_type"],
        cpu_required=final_requirements["cpu_required"],
        memory_required_gb=final_requirements["memory_required_gb"],
        gpu_required=final_requirements["gpu_required"],
        deadline_seconds=final_requirements["deadline_seconds"],
        priority=final_requirements["priority"]
    )

    print("\nTask Created:")
    task.display_info()


    # --------------------------------------------------
    # Step 7: Create QoS Scheduler
    # --------------------------------------------------

    scheduler = QoSScheduler(nodes)


    # --------------------------------------------------
    # Step 8: Get node rankings
    # --------------------------------------------------

    rankings = scheduler.get_node_rankings(task)


    print("\nNode Rankings:")
    print("-" * 60)

    for ranking in rankings:

        print(
            f"Node: {ranking['node'].node_id} | "
            f"Resource Score: {ranking['resource_score']:.2f} | "
            f"Priority Score: {ranking['priority_score']:.2f} | "
            f"Deadline Score: {ranking['deadline_score']:.2f} | "
            f"Final Score: {ranking['final_score']:.2f}"
        )


    # --------------------------------------------------
    # Step 9: Select best node
    # --------------------------------------------------

    best_node = scheduler.select_best_node(task)


    print("\nSelected Node:")
    print(best_node.node_id)


    print("\n" + "=" * 60)
    print("LLM + QOS SCHEDULER INTEGRATION PASSED")
    print("=" * 60)


except Exception as error:

    print("\nERROR:")
    print(error)