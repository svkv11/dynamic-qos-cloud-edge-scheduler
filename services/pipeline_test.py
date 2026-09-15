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


from scheduler.compute_node import (
    ComputeNode
)

from scheduling_pipeline import (
    SchedulingPipeline
)


print("=" * 70)
print("REUSABLE SCHEDULING PIPELINE + EXECUTION TEST")
print("=" * 70)


# ------------------------------------------------------
# Step 1: Create compute nodes
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
# Step 3: Create reusable pipeline
# ------------------------------------------------------

pipeline = SchedulingPipeline(
    nodes
)


# ------------------------------------------------------
# Step 4: Test natural-language request
# ------------------------------------------------------

user_request = (
    "Create an AI image quickly."
)

print("\nUser Request:")
print(user_request)


try:

    # --------------------------------------------------
    # Step 5: Process complete request
    # --------------------------------------------------

    result = pipeline.process_request(
        user_request=user_request,
        task_id="pipeline-task-001"
    )


    # --------------------------------------------------
    # Step 6: Display LLM interpretation
    # --------------------------------------------------

    print("\nLLM Interpretation:")
    print(
        result[
            "interpreted_requirements"
        ]
    )


    # --------------------------------------------------
    # Step 7: Display final requirements
    # --------------------------------------------------

    print("\nFinal Requirements:")
    print(
        result[
            "final_requirements"
        ]
    )


    # --------------------------------------------------
    # Step 8: Display Task
    # --------------------------------------------------

    print("\nCreated Task:")
    result["task"].display_info()


    # --------------------------------------------------
    # Step 9: Display rankings
    # --------------------------------------------------

    print("\nNode Rankings:")
    print("-" * 70)

    for ranking in result["rankings"]:

        print(
            f"Node: "
            f"{ranking['node'].node_id} | "
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
    # Step 10: Display selected node
    # --------------------------------------------------

    print("\nSelected Node:")

    print(
        result[
            "selected_node"
        ].node_id
    )


    # --------------------------------------------------
    # Step 11: Display execution result
    # --------------------------------------------------

    execution_result = result[
        "execution_result"
    ]

    print("\nExecution Result:")
    print("-" * 70)

    print(
        f"Task ID: "
        f"{execution_result['task_id']}"
    )

    print(
        f"Node ID: "
        f"{execution_result['node_id']}"
    )

    print(
        f"Execution Time: "
        f"{execution_result['execution_time']} seconds"
    )

    print(
        f"Deadline: "
        f"{execution_result['deadline_seconds']}"
    )

    print(
        f"Deadline Met: "
        f"{execution_result['deadline_met']}"
    )

    print(
        f"Final State: "
        f"{execution_result['state']}"
    )

    print(
        f"Failure Reason: "
        f"{execution_result['failure_reason']}"
    )


    print("\n" + "=" * 70)
    print("PIPELINE + EXECUTION TEST PASSED")
    print("=" * 70)


except Exception as error:

    print("\nERROR:")
    print(error)