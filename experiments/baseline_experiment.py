from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
from scheduler.baseline_scheduler import BaselineScheduler
from scheduler.task_executor import TaskExecutor

from experiments.experiment_scenarios import ExperimentScenarios


class BaselineExperiment:
    """
    Compare simple baseline scheduling strategies
    with the Dynamic QoS Scheduler.
    """

    def get_scenario_conditions(self, scenario_name):
        scenarios = {
            "normal": ExperimentScenarios.normal,
            "high_cpu": ExperimentScenarios.high_cpu,
            "high_memory": ExperimentScenarios.high_memory,
            "high_latency": ExperimentScenarios.high_latency,
            "tight_deadline": ExperimentScenarios.tight_deadline,
            "priority_conflict": ExperimentScenarios.priority_conflict,
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
        return ExperimentScenarios.get_task_profile(
            scenario_name
        )

    def create_nodes(self, resource_conditions):
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

    def execute_assignment(
        self,
        task,
        node,
        qos_score
    ):
        if node is None:
            return {
                "task_id": task.task_id,
                "node_id": None,
                "selection_qos_score": qos_score,
                "execution_time": None,
                "deadline_met": False,
                "state": "FAILED"
            }

        if not node.allocate_task(task):
            return {
                "task_id": task.task_id,
                "node_id": node.node_id,
                "selection_qos_score": qos_score,
                "execution_time": None,
                "deadline_met": False,
                "state": "FAILED"
            }

        executor = TaskExecutor()

        task_state = executor.start_task(
            task,
            node
        )

        result = executor.complete_task(
            task_state
        )

        return {
            "task_id": task.task_id,
            "node_id": node.node_id,
            "selection_qos_score": qos_score,
            "execution_time": result["execution_time"],
            "deadline_met": result["deadline_met"],
            "state": result["state"]
        }

    def run_round_robin(self, scenario_name):
        conditions = self.get_scenario_conditions(
            scenario_name
        )

        task_profile = self.get_task_profile(
            scenario_name
        )

        nodes = self.create_nodes(conditions)
        tasks = self.create_tasks(task_profile)

        scheduler = BaselineScheduler(nodes)

        assignments = scheduler.round_robin(tasks)

        results = []

        for assignment in assignments:
            task = assignment["task"]
            node = assignment["node"]

            results.append(
                self.execute_assignment(
                    task=task,
                    node=node,
                    qos_score=None
                )
            )

        return self.build_summary(
            scenario_name,
            "round_robin",
            results
        )

    def run_resource_only(self, scenario_name):
        conditions = self.get_scenario_conditions(
            scenario_name
        )

        task_profile = self.get_task_profile(
            scenario_name
        )

        nodes = self.create_nodes(conditions)
        tasks = self.create_tasks(task_profile)

        scheduler = BaselineScheduler(nodes)

        assignments = scheduler.resource_only(tasks)

        results = []

        for assignment in assignments:
            task = assignment["task"]
            node = assignment["node"]
            resource_score = assignment["resource_score"]

            results.append(
                self.execute_assignment(
                    task=task,
                    node=node,
                    qos_score=resource_score
                )
            )

        return self.build_summary(
            scenario_name,
            "resource_only",
            results
        )

    def run_dynamic_qos(self, scenario_name):
        conditions = self.get_scenario_conditions(
            scenario_name
        )

        task_profile = self.get_task_profile(
            scenario_name
        )

        nodes = self.create_nodes(conditions)
        tasks = self.create_tasks(task_profile)

        scheduler = QoSScheduler(nodes)

        results = []

        for task in tasks:

            rankings = scheduler.get_node_rankings(
                task
            )

            if not rankings:
                results.append(
                    self.execute_assignment(
                        task=task,
                        node=None,
                        qos_score=None
                    )
                )
                continue

            selected = rankings[0]

            node = selected["node"]
            selection_qos_score = selected["final_score"]

            results.append(
                self.execute_assignment(
                    task=task,
                    node=node,
                    qos_score=selection_qos_score
                )
            )

        return self.build_summary(
            scenario_name,
            "dynamic_qos",
            results
        )

    def build_summary(
        self,
        scenario_name,
        strategy_name,
        results
    ):
        valid_results = [
            result
            for result in results
            if result["execution_time"] is not None
        ]

        completed_tasks = sum(
            1
            for result in results
            if result["state"] == "COMPLETED"
        )

        failed_tasks = sum(
            1
            for result in results
            if result["state"] == "FAILED"
        )

        if valid_results:
            deadline_success_rate = round(
                sum(
                    1
                    for result in valid_results
                    if result["deadline_met"]
                )
                / len(valid_results)
                * 100,
                2
            )
        else:
            deadline_success_rate = 0.0

        if valid_results:
            average_execution_time = round(
                sum(
                    result["execution_time"]
                    for result in valid_results
                )
                / len(valid_results),
                2
            )
        else:
            average_execution_time = 0.0

        qos_results = [
            result["selection_qos_score"]
            for result in valid_results
            if result["selection_qos_score"] is not None
        ]

        if qos_results:
            average_qos_score = round(
                sum(qos_results)
                / len(qos_results),
                2
            )
        else:
            average_qos_score = 0.0

        node_usage = {}

        for result in valid_results:
            node_id = result["node_id"]

            if node_id not in node_usage:
                node_usage[node_id] = 0

            node_usage[node_id] += 1

        return {
            "scenario": scenario_name,
            "strategy": strategy_name,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "deadline_success_rate": deadline_success_rate,
            "average_execution_time": average_execution_time,
            "average_qos_score": average_qos_score,
            "node_usage": node_usage,
            "task_results": results
        }

    def run_scenario(self, scenario_name):
        return {
            "round_robin": self.run_round_robin(
                scenario_name
            ),
            "resource_only": self.run_resource_only(
                scenario_name
            ),
            "dynamic_qos": self.run_dynamic_qos(
                scenario_name
            )
        }


if __name__ == "__main__":
    experiment = BaselineExperiment()

    results = experiment.run_scenario("normal")

    print("=" * 70)
    print("BASELINE SCHEDULER COMPARISON")
    print("=" * 70)

    for strategy, result in results.items():
        print(
            f"{strategy:<20}"
            f"Completed={result['completed_tasks']:<5}"
            f"Failed={result['failed_tasks']:<5}"
            f"Deadline={result['deadline_success_rate']:<6}"
            f"Avg Time={result['average_execution_time']:<6}"
            f"Selection QoS={result['average_qos_score']}"
        )

    print("=" * 70)