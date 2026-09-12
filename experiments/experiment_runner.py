from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
from scheduler.task_executor import TaskExecutor
from scheduler.worker import Worker
from scheduler.worker_manager import WorkerManager
from scheduler.scheduling_controller import SchedulingController

from experiments.experiment_scenarios import ExperimentScenarios


class ExperimentRunner:
    """
    Run controlled scheduler experiments and collect results.
    """

    def get_scenario_conditions(self, scenario_name):
        """
        Return resource conditions for the requested scenario.
        """

        scenarios = {
            "normal": ExperimentScenarios.normal,
            "high_cpu": ExperimentScenarios.high_cpu,
            "high_memory": ExperimentScenarios.high_memory,
            "high_latency": ExperimentScenarios.high_latency,
            "tight_deadline": ExperimentScenarios.tight_deadline,
            "priority_conflict":
                ExperimentScenarios.priority_conflict,
            "resource_deadline_pressure":
                ExperimentScenarios.resource_deadline_pressure
        }

        if scenario_name not in scenarios:
            raise ValueError(
                f"Unknown scenario: {scenario_name}. "
                f"Available scenarios: {list(scenarios.keys())}"
            )

        return scenarios[scenario_name]()

    def get_task_profile(self, scenario_name):
        """
        Return the workload profile associated with
        the selected experiment scenario.
        """

        return ExperimentScenarios.get_task_profile(
            scenario_name
        )

    def create_nodes(self, resource_conditions=None):
        """
        Create the standard cloud-edge node configuration.

        Dynamic resource values are taken from the selected
        experiment scenario.
        """

        if resource_conditions is None:
            resource_conditions = (
                ExperimentScenarios.normal()
            )

        return [
            ComputeNode(
                node_id="edge-01",
                node_type="edge",
                cpu_cores=4,
                memory_gb=8,
                gpu_available=False,
                cpu_utilization=resource_conditions["edge-01"][
                    "cpu_utilization"
                ],
                memory_utilization=resource_conditions["edge-01"][
                    "memory_utilization"
                ],
                gpu_utilization=resource_conditions["edge-01"][
                    "gpu_utilization"
                ],
                network_latency_ms=resource_conditions["edge-01"][
                    "network_latency_ms"
                ]
            ),
            ComputeNode(
                node_id="edge-02",
                node_type="edge",
                cpu_cores=8,
                memory_gb=16,
                gpu_available=True,
                cpu_utilization=resource_conditions["edge-02"][
                    "cpu_utilization"
                ],
                memory_utilization=resource_conditions["edge-02"][
                    "memory_utilization"
                ],
                gpu_utilization=resource_conditions["edge-02"][
                    "gpu_utilization"
                ],
                network_latency_ms=resource_conditions["edge-02"][
                    "network_latency_ms"
                ]
            ),
            ComputeNode(
                node_id="cloud-01",
                node_type="cloud",
                cpu_cores=16,
                memory_gb=32,
                gpu_available=True,
                cpu_utilization=resource_conditions["cloud-01"][
                    "cpu_utilization"
                ],
                memory_utilization=resource_conditions["cloud-01"][
                    "memory_utilization"
                ],
                gpu_utilization=resource_conditions["cloud-01"][
                    "gpu_utilization"
                ],
                network_latency_ms=resource_conditions["cloud-01"][
                    "network_latency_ms"
                ]
            )
        ]

    def create_tasks(self, task_profile="normal"):
        """
        Create the heterogeneous workload associated
        with the selected experiment profile.
        """

        if task_profile == "normal":
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

        if task_profile == "tight_deadline":
            return [
                Task(
                    task_id="task-01",
                    workload_type="cpu_intensive",
                    cpu_required=2,
                    memory_required_gb=2,
                    gpu_required=False,
                    deadline_seconds=6,
                    priority=2
                ),
                Task(
                    task_id="task-02",
                    workload_type="memory_intensive",
                    cpu_required=2,
                    memory_required_gb=4,
                    gpu_required=False,
                    deadline_seconds=7,
                    priority=3
                ),
                Task(
                    task_id="task-03",
                    workload_type="gpu_intensive",
                    cpu_required=4,
                    memory_required_gb=8,
                    gpu_required=True,
                    deadline_seconds=8,
                    priority=4
                ),
                Task(
                    task_id="task-04",
                    workload_type="latency_sensitive",
                    cpu_required=1,
                    memory_required_gb=2,
                    gpu_required=False,
                    deadline_seconds=4,
                    priority=5
                )
            ]

        if task_profile == "priority_conflict":
            return [
                Task(
                    task_id="task-01",
                    workload_type="cpu_intensive",
                    cpu_required=2,
                    memory_required_gb=2,
                    gpu_required=False,
                    deadline_seconds=60,
                    priority=5
                ),
                Task(
                    task_id="task-02",
                    workload_type="memory_intensive",
                    cpu_required=2,
                    memory_required_gb=4,
                    gpu_required=False,
                    deadline_seconds=60,
                    priority=1
                ),
                Task(
                    task_id="task-03",
                    workload_type="gpu_intensive",
                    cpu_required=4,
                    memory_required_gb=8,
                    gpu_required=True,
                    deadline_seconds=30,
                    priority=5
                ),
                Task(
                    task_id="task-04",
                    workload_type="latency_sensitive",
                    cpu_required=1,
                    memory_required_gb=2,
                    gpu_required=False,
                    deadline_seconds=15,
                    priority=1
                )
            ]

        raise ValueError(
            f"Unknown task profile: {task_profile}"
        )

    def run_experiment(self, scenario_name="normal"):
        """
        Run one scheduler experiment using the selected
        resource scenario and workload profile.

        Returns the collected experiment metrics and
        node-selection information.
        """

        resource_conditions = self.get_scenario_conditions(
            scenario_name
        )

        task_profile = self.get_task_profile(
            scenario_name
        )

        nodes = self.create_nodes(
            resource_conditions
        )

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

        tasks = self.create_tasks(
            task_profile
        )

        initial_rankings = {}

        for task in tasks:
            rankings = scheduler.get_node_rankings(task)

            initial_rankings[task.task_id] = [
                {
                    "node_id": item["node"].node_id,
                    "final_score": item["final_score"]
                }
                for item in rankings
            ]

            scheduler.add_task(task)

        completed = controller.run_cycle()

        metrics = controller.get_metrics()

        return {
            "scenario": scenario_name,
            "task_profile": task_profile,
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
            "node_usage": metrics.get_node_usage(),
            "initial_rankings": initial_rankings
        }

    def display_result(self, result):
        """
        Display experiment results in a readable format.
        """

        print("=" * 60)
        print("EXPERIMENT RESULT")
        print("=" * 60)

        print(
            f"Scenario: "
            f"{result['scenario']}"
        )

        print(
            f"Task Profile: "
            f"{result['task_profile']}"
        )

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

        print()
        print("Initial Node Rankings:")

        for task_id, rankings in result[
            "initial_rankings"
        ].items():

            ranking_text = " > ".join(
                f"{item['node_id']} "
                f"({item['final_score']})"
                for item in rankings
            )

            print(
                f"  {task_id}: "
                f"{ranking_text}"
            )

        print("=" * 60)