import os
import sys

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


print("=" * 80)
print("GENAI MULTI-WORKLOAD EVALUATION")
print("=" * 80)


# --------------------------------------------------
# Create compute nodes
# --------------------------------------------------

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


# --------------------------------------------------
# Configure node states
# --------------------------------------------------

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


# --------------------------------------------------
# Natural-language workload requests
# --------------------------------------------------

test_requests = [
    "Create an AI image quickly.",

    "Analyze a very large dataset that requires "
    "a lot of RAM.",

    "Process this CPU-heavy workload using "
    "6 CPU cores.",

    "Run the deep learning model using GPU "
    "within 15 seconds.",

    "Run this task as urgently as possible."
]


# --------------------------------------------------
# Create pipeline
# --------------------------------------------------

pipeline = SchedulingPipeline(
    nodes
)


# --------------------------------------------------
# Process each request
# --------------------------------------------------

for index, user_request in enumerate(
    test_requests,
    start=1
):

    print("\n")
    print("=" * 80)
    print(f"TEST CASE {index}")
    print("=" * 80)

    print("\nUser Request:")
    print(user_request)

    try:

        result = pipeline.process_request(
            user_request=user_request,
            task_id=f"genai-task-{index:03d}"
        )

        # --------------------------------------------------
        # LLM interpretation
        # --------------------------------------------------

        interpreted = result[
            "interpreted_requirements"
        ]

        print("\nLLM Interpretation:")
        print(interpreted)


        # --------------------------------------------------
        # Final requirements
        # --------------------------------------------------

        final_requirements = result[
            "final_requirements"
        ]

        print("\nFinal Requirements:")
        print(final_requirements)


        # --------------------------------------------------
        # Selected node
        # --------------------------------------------------

        selected_node = result[
            "selected_node"
        ]

        print("\nSelected Node:")
        print(
            f"{selected_node.node_id} "
            f"({selected_node.node_type})"
        )


        # --------------------------------------------------
        # Execution result
        # --------------------------------------------------

        execution_result = result[
            "execution_result"
        ]

        print("\nExecution Result:")
        print("-" * 80)

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
            f"QoS Score: "
            f"{result['qos_score']:.2f}"
        )


    except Exception as error:

        print("\nERROR:")
        print(error)


# --------------------------------------------------
# Final evaluation summary
# --------------------------------------------------

print("\n")
print("=" * 80)
print("OVERALL GENAI EVALUATION SUMMARY")
print("=" * 80)

metrics = pipeline.get_metrics()

metrics.display_summary()


# --------------------------------------------------
# Display every recorded metric
# --------------------------------------------------

print("\nDetailed Recorded Results:")
print("-" * 80)

records = metrics.get_records()

for record in records:

    print(
        f"Task: {record['task_id']} | "
        f"Workload: {record['workload_type']} | "
        f"Node: {record['node_id']} | "
        f"Time: {record['execution_time']}s | "
        f"Deadline Met: {record['deadline_met']} | "
        f"Priority: {record['priority']} | "
        f"QoS: {record['qos_score']} | "
        f"State: {record['state']}"
    )


print("\n" + "=" * 80)
print("GENAI MULTI-WORKLOAD EVALUATION COMPLETED")
print("=" * 80)