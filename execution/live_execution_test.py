from scheduler.task import Task
from scheduler.compute_node import ComputeNode

from execution.workload_runner import WorkloadRunner


def main():
    print("=" * 60)
    print("LIVE EXECUTION TEST")
    print("=" * 60)

    # Create a sample task
    task = Task(
        task_id="live-test-01",
        workload_type="general",
        cpu_required=2,
        memory_required_gb=2,
        gpu_required=False,
        deadline_seconds=10,
        priority=3
    )

    # Create a logical node
    node = ComputeNode(
        node_id="edge-01",
        node_type="edge",
        cpu_cores=4,
        memory_gb=8,
        gpu_available=False,
        cpu_utilization=25,
        memory_utilization=30,
        gpu_utilization=0,
        network_latency_ms=10
    )

    # Run the real workload
    runner = WorkloadRunner()

    result = runner.run(
        task=task,
        node=node
    )

    # Display the real execution result
    result.display()


if __name__ == "__main__":
    main()