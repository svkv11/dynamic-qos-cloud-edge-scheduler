from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
from scheduler.task_executor import TaskExecutor
from scheduler.worker import Worker
from scheduler.worker_manager import WorkerManager
from scheduler.scheduling_controller import SchedulingController


class ExperimentRunner:
    """
    Run controlled scheduler experiments and collect results.
    """

    def create_nodes(self):
        """
        Create the standard cloud-edge node configuration
        used for experiments.
        """

        return [
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

    def create_tasks(self):
        """
        Create a standard heterogeneous workload
        for the experiment.
        """

        return [
            Task(
                task_id="task-01",
                workload_type="cpu_intensive",
                cpu_required=2,
                memory_required_gb=2,
                gpu_required=False,
                deadline_seconds=60,
                priority=2
            ),
            Task(
                task_id="task-02",
                workload_type="memory_intensive",
                cpu_required=2,
                memory_required_gb=4,
                gpu_required=False,
                deadline_seconds=60,
                priority=3
            ),
            Task(
                task_id="task-03",
                workload_type="gpu_intensive",
                cpu_required=4,
                memory_required_gb=8,
                gpu_required=True,
                deadline_seconds=30,
                priority=4
            ),
            Task(
                task_id="task-04",
                workload_type="latency_sensitive",
                cpu_required=1,
                memory_required_gb=2,
                gpu_required=False,
                deadline_seconds=15,
                priority=5
            )
        ]

    def run_experiment(self):
        """
        Run one standard scheduler experiment.

        Returns the collected experiment metrics.
        """

        nodes = self.create_nodes()

        scheduler = QoSScheduler(nodes)
        executor = TaskExecutor()

        workers = [
            Worker("worker-01", nodes[0]),
            Worker("worker-02", nodes[1]),
            Worker("worker-03", nodes[2])
        ]

        worker_manager = WorkerManager(workers)

        controller = SchedulingController(
            scheduler=scheduler,
            executor=executor,
            worker_manager=worker_manager
        )

        controller.start_workers()

        tasks = self.create_tasks()

        for task in tasks:
            scheduler.add_task(task)

        completed = controller.run_cycle()

        metrics = controller.get_metrics()

        return {
            "completed_during_cycle": completed,
            "total_tasks": metrics.get_total_tasks(),
            "completed_tasks": metrics.get_completed_tasks(),
            "failed_tasks": metrics.get_failed_tasks(),
            "deadline_success_rate": (
                metrics.get_deadline_success_rate()
            ),
            "average_execution_time": (
                metrics.get_average_execution_time()
            ),
            "average_qos_score": (
                metrics.get_average_qos_score()
            ),
            "node_usage": metrics.get_node_usage()
        }

    def display_result(self, result):
        """
        Display experiment results in a readable format.
        """

        print("=" * 60)
        print("EXPERIMENT RESULT")
        print("=" * 60)

        print(
            f"Completed During Cycle: "
            f"{result['completed_during_cycle']}"
        )

        print(
            f"Total Tasks: "
            f"{result['total_tasks']}"
        )

        print(
            f"Completed Tasks: "
            f"{result['completed_tasks']}"
        )

        print(
            f"Failed Tasks: "
            f"{result['failed_tasks']}"
        )

        print(
            f"Deadline Success Rate: "
            f"{result['deadline_success_rate']}%"
        )

        print(
            f"Average Execution Time: "
            f"{result['average_execution_time']} seconds"
        )

        print(
            f"Average QoS Score: "
            f"{result['average_qos_score']}"
        )

        print("Node Usage:")

        for node_id, count in result["node_usage"].items():
            print(
                f"  {node_id}: "
                f"{count} task(s)"
            )

        print("=" * 60)