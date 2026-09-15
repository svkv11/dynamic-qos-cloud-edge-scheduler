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
print("GENAI + QOS + DEADLINE EXECUTION TEST")
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
# Set node states
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
# Create pipeline
# ------------------------------------------------------

pipeline = SchedulingPipeline(
    nodes
)


# ------------------------------------------------------
# Natural-language request
# ------------------------------------------------------

user_request = (
    "Run the deep learning model using GPU "
    "within 15 seconds."
)


print("\nUser Request:")
print(user_request)


try:

    # --------------------------------------------------
    # Process request
    # --------------------------------------------------

    result = pipeline.process_request(
        user_request=user_request,
        task_id="deadline-task-001"
    )


    # --------------------------------------------------
    # Display interpretation
    # --------------------------------------------------

    print("\nLLM Interpretation:")
    print(
        result[
            "interpreted_requirements"
        ]
    )


    # --------------------------------------------------
    # Display final requirements
    # --------------------------------------------------

    print("\nFinal Requirements:")
    print(
        result[
            "final_requirements"
        ]
    )


    # --------------------------------------------------
    # Display selected node
    # --------------------------------------------------

    print("\nSelected Node:")
    print(
        result[
            "selected_node"
        ].node_id
    )


    # --------------------------------------------------
    # Display execution result
    # --------------------------------------------------

    execution_result = (
        result[
            "execution_result"
        ]
    )

    print("\nExecution Result:")
    print("-" * 70)

    print(
        f"Execution Time: "
        f"{execution_result['execution_time']} seconds"
    )

    print(
        f"Deadline: "
        f"{execution_result['deadline_seconds']} seconds"
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
    print("DEADLINE PIPELINE TEST COMPLETED")
    print("=" * 70)


except Exception as error:

    print("\nERROR:")
    print(error)