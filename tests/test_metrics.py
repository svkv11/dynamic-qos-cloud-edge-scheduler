from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.metrics import MetricsCollector


node = ComputeNode(
    node_id="edge-01",
    node_type="edge",
    cpu_cores=4,
    memory_gb=8,
    gpu_available=False,
    cpu_utilization=25.0,
    memory_utilization=30.0,
    gpu_utilization=0.0,
    network_latency_ms=10.0
)

task_1 = Task(
    task_id="task-01",
    workload_type="cpu_intensive",
    cpu_required=2,
    memory_required_gb=2,
    deadline_seconds=20,
    priority=3
)

task_1.state = "COMPLETED"

task_2 = Task(
    task_id="task-02",
    workload_type="memory_intensive",
    cpu_required=1,
    memory_required_gb=4,
    deadline_seconds=10,
    priority=4
)

task_2.state = "COMPLETED"


metrics = MetricsCollector()

metrics.record_task(
    task=task_1,
    node=node,
    execution_time=8.0,
    deadline_met=True,
    qos_score=82.5
)

metrics.record_task(
    task=task_2,
    node=node,
    execution_time=12.0,
    deadline_met=False,
    qos_score=75.0
)


print("=" * 60)
print("METRICS COLLECTOR TEST")
print("=" * 60)

print()
print("Recorded Task Results")

for record in metrics.get_records():
    print(record)

print()

metrics.display_summary()

print()
print("=" * 60)
print("TEST RESULT")
print("=" * 60)

if (
    metrics.get_total_tasks() == 2
    and metrics.get_completed_tasks() == 2
    and metrics.get_failed_tasks() == 0
    and metrics.get_deadline_success_rate() == 50.0
    and metrics.get_average_execution_time() == 10.0
    and metrics.get_average_qos_score() == 78.75
    and metrics.get_node_usage()["edge-01"] == 2
):
    print("Metrics Collector Test: PASSED")
else:
    print("Metrics Collector Test: FAILED")

print("=" * 60)