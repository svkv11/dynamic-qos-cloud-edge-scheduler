from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.baseline_scheduler import BaselineScheduler


def create_test_nodes():
    return [
        ComputeNode(
            node_id="edge-01",
            node_type="edge",
            cpu_cores=4,
            memory_gb=8,
            gpu_available=False,
            cpu_utilization=20.0,
            memory_utilization=20.0,
            gpu_utilization=0.0,
            network_latency_ms=10.0
        ),
        ComputeNode(
            node_id="edge-02",
            node_type="edge",
            cpu_cores=8,
            memory_gb=16,
            gpu_available=True,
            cpu_utilization=30.0,
            memory_utilization=30.0,
            gpu_utilization=10.0,
            network_latency_ms=15.0
        ),
        ComputeNode(
            node_id="cloud-01",
            node_type="cloud",
            cpu_cores=16,
            memory_gb=32,
            gpu_available=True,
            cpu_utilization=50.0,
            memory_utilization=50.0,
            gpu_utilization=30.0,
            network_latency_ms=80.0
        )
    ]


def test_round_robin():
    nodes = create_test_nodes()
    scheduler = BaselineScheduler(nodes)

    tasks = [
        Task(
            task_id="task-01",
            workload_type="cpu_intensive",
            cpu_required=1,
            memory_required_gb=1
        ),
        Task(
            task_id="task-02",
            workload_type="memory_intensive",
            cpu_required=1,
            memory_required_gb=1
        ),
        Task(
            task_id="task-03",
            workload_type="gpu_intensive",
            cpu_required=1,
            memory_required_gb=1,
            gpu_required=True
        )
    ]

    assignments = scheduler.round_robin(tasks)

    selected_nodes = [
        assignment["node"].node_id
        for assignment in assignments
    ]

    print("Round Robin Assignments:")
    for assignment in assignments:
        print(
            f"  {assignment['task'].task_id} -> "
            f"{assignment['node'].node_id}"
        )

    assert selected_nodes == [
        "edge-01",
        "edge-02",
        "cloud-01"
    ]

    print("Round Robin Test: PASSED")


def test_resource_only():
    nodes = create_test_nodes()
    scheduler = BaselineScheduler(nodes)

    task = Task(
        task_id="task-gpu",
        workload_type="gpu_intensive",
        cpu_required=2,
        memory_required_gb=4,
        gpu_required=True
    )

    assignments = scheduler.resource_only([task])

    assignment = assignments[0]

    print()
    print("Resource-Only Assignment:")
    print(
        f"  {task.task_id} -> "
        f"{assignment['node'].node_id}"
    )
    print(
        f"  Resource Score: "
        f"{assignment['resource_score']}"
    )

    assert assignment["node"].node_id == "edge-02"

    print("Resource-Only Test: PASSED")


def test_infeasible_node_is_skipped():
    nodes = create_test_nodes()

    nodes[0].cpu_utilization = 100.0
    nodes[0].memory_utilization = 100.0

    scheduler = BaselineScheduler(nodes)

    task = Task(
        task_id="task-01",
        workload_type="cpu_intensive",
        cpu_required=1,
        memory_required_gb=1
    )

    assignments = scheduler.resource_only([task])

    assignment = assignments[0]

    print()
    print("Infeasible Node Test:")
    print(
        f"  Selected Node: "
        f"{assignment['node'].node_id}"
    )

    assert assignment["node"].node_id != "edge-01"

    print("Infeasible Node Test: PASSED")


def run_tests():
    print("=" * 60)
    print("BASELINE SCHEDULER TEST")
    print("=" * 60)

    test_round_robin()
    test_resource_only()
    test_infeasible_node_is_skipped()

    print("=" * 60)
    print("Baseline Scheduler Tests: ALL PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()