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


print("=" * 70)
print("MULTI-WORKLOAD LLM + QOS END-TO-END TEST")
print("=" * 70)


# ------------------------------------------------------
# Create compute nodes
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
# Set current node states
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
# Natural-language workload requests
# ------------------------------------------------------

test_requests = [
    "Create an AI image quickly.",

    "Analyze a very large dataset that requires a lot of RAM.",

    "Process this CPU-heavy workload using 6 CPU cores.",

    "Run the deep learning model using GPU within 15 seconds.",

    "Run this task as urgently as possible."
]


# ------------------------------------------------------
# Create scheduler
# ------------------------------------------------------

scheduler = QoSScheduler(nodes)


# ------------------------------------------------------
# Process each request
# ------------------------------------------------------

for index, user_request in enumerate(
    test_requests,
    start=1
):

    print("\n")
    print("=" * 70)
    print(f"TEST CASE {index}")
    print("=" * 70)

    print("\nUser Request:")
    print(user_request)

    try:

        # --------------------------------------------------
        # Step 1: LLM interpretation
        # --------------------------------------------------

        interpreted_requirements = (
            LLMRequirementInterpreter.interpret(
                user_request
            )
        )

        print("\nLLM Interpretation:")
        print(interpreted_requirements)


        # --------------------------------------------------
        # Step 2: Workload profiling
        # --------------------------------------------------

        final_requirements = (
            WorkloadProfiler.build_requirements(
                interpreted_requirements
            )
        )

        print("\nFinal Profiled Requirements:")
        print(final_requirements)


        # --------------------------------------------------
        # Step 3: Create Task
        # --------------------------------------------------

        task = Task(
            task_id=f"llm-task-{index:03d}",
            workload_type=final_requirements[
                "workload_type"
            ],
            cpu_required=final_requirements[
                "cpu_required"
            ],
            memory_required_gb=final_requirements[
                "memory_required_gb"
            ],
            gpu_required=final_requirements[
                "gpu_required"
            ],
            deadline_seconds=final_requirements[
                "deadline_seconds"
            ],
            priority=final_requirements[
                "priority"
            ]
        )

        print("\nCreated Task:")
        task.display_info()


        # --------------------------------------------------
        # Step 4: Calculate node rankings
        # --------------------------------------------------

        rankings = scheduler.get_node_rankings(
            task
        )


        print("\nNode Rankings:")
        print("-" * 70)

        for ranking in rankings:

            print(
                f"Node: {ranking['node'].node_id} | "
                f"Resource: "
                f"{ranking['resource_score']:.2f} | "
                f"Priority: "
                f"{ranking['priority_score']:.2f} | "
                f"Deadline: "
                f"{ranking['deadline_score']:.2f} | "
                f"Final: "
                f"{ranking['final_score']:.2f}"
            )


        # --------------------------------------------------
        # Step 5: Select best node
        # --------------------------------------------------

        best_node = scheduler.select_best_node(
            task
        )


        print("\nSelected Node:")
        print(best_node.node_id)


    except Exception as error:

        print("\nERROR:")
        print(error)


print("\n")
print("=" * 70)
print("MULTI-WORKLOAD TEST COMPLETED")
print("=" * 70)