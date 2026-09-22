import csv
from pathlib import Path

from scheduler.compute_node import ComputeNode
from scheduler.task import Task
from scheduler.scheduler import QoSScheduler
from scheduler.baseline_scheduler import BaselineScheduler
from scheduler.task_executor import TaskExecutor

from experiments.experiment_scenarios import ExperimentScenarios


class AblationExperiment:
    """
    Controlled ablation study for the Dynamic QoS Scheduler.

    Variants:
        full
            Resource + Priority + Node-aware Deadline

        no_priority
            Resource + Node-aware Deadline

        no_deadline
            Resource + Priority

        resource_only
            Resource suitability only

    Selection scores and evaluation metrics are kept separate.

    Selection score:
        The score actually used by each strategy to select a node.

    Evaluation metrics:
        - Resource suitability score
        - Full Dynamic QoS score
        - Estimated execution time
        - Deadline success

    The same scenarios, workloads, node configurations,
    and execution mechanism are used across strategies.

    The deadline_resource_tradeoff scenario is a dedicated
    controlled experiment designed to test whether node-aware
    deadline performance can change the scheduling decision
    when a high-resource node and a low-latency node are
    both feasible.
    """

    STRATEGIES = [
        "full",
        "no_priority",
        "no_deadline",
        "resource_only"
    ]

    SCENARIOS = [
        "normal",
        "high_cpu",
        "high_memory",
        "high_latency",
        "tight_deadline",
        "priority_conflict",
        "resource_deadline_pressure",
        "deadline_resource_tradeoff"
    ]

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

        if scenario_name == "deadline_resource_tradeoff":
            return None

        if scenario_name not in scenarios:
            raise ValueError(
                f"Unknown scenario: {scenario_name}. "
                f"Available scenarios: {list(scenarios.keys())}"
            )

        return scenarios[scenario_name]()

    def get_task_profile(self, scenario_name):
        if scenario_name == "deadline_resource_tradeoff":
            return "deadline_resource_tradeoff"

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

    def create_tradeoff_nodes(self):
        """
        Create controlled nodes for the deadline/resource
        trade-off experiment.

        edge-01:
            Lower resource suitability but very low latency.

        cloud-01:
            Higher resource suitability but high latency.

        Both nodes are feasible for the task.
        """

        return [
            ComputeNode(
                node_id="edge-01",
                node_type="edge",
                cpu_cores=8,
                memory_gb=8,
                gpu_available=True,
                cpu_utilization=50.0,
                memory_utilization=50.0,
                gpu_utilization=80.0,
                network_latency_ms=5.0
            ),
            ComputeNode(
                node_id="cloud-01",
                node_type="cloud",
                cpu_cores=16,
                memory_gb=32,
                gpu_available=True,
                cpu_utilization=20.0,
                memory_utilization=20.0,
                gpu_utilization=10.0,
                network_latency_ms=80.0
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

        if task_profile == "deadline_resource_tradeoff":
            return [
                Task(
                    task_id="tradeoff-task",
                    workload_type="gpu_intensive",
                    cpu_required=4,
                    memory_required_gb=4,
                    gpu_required=True,
                    deadline_seconds=10,
                    priority=5
                )
            ]

        raise ValueError(
            f"Unknown task profile: {task_profile}"
        )

    def calculate_evaluation_scores(self, task, node):
        """
        Calculate common evaluation metrics for a selected node.

        These metrics are calculated after node selection and are
        independent of which strategy selected the node.

        resource_suitability_score:
            The resource-only component from ComputeNode.

        dynamic_qos_score:
            The full Dynamic QoS score using the complete
            scheduler formulation.
        """

        if node is None:
            return {
                "resource_suitability_score": None,
                "dynamic_qos_score": None
            }

        resource_score = node.calculate_qos_score(task)

        evaluation_scheduler = QoSScheduler(
            [node],
            mode="full"
        )

        dynamic_qos_score = evaluation_scheduler.calculate_task_score(
            node,
            task
        )

        return {
            "resource_suitability_score": resource_score,
            "dynamic_qos_score": dynamic_qos_score
        }

    def execute_assignment(
        self,
        task,
        node,
        selection_score,
        selection_score_type
    ):
        if node is None:
            return {
                "task_id": task.task_id,
                "node_id": None,
                "selection_score": selection_score,
                "selection_score_type": selection_score_type,
                "resource_suitability_score": None,
                "dynamic_qos_score": None,
                "execution_time": None,
                "deadline_met": False,
                "state": "FAILED"
            }

        evaluation_scores = self.calculate_evaluation_scores(
            task,
            node
        )

        if not node.allocate_task(task):
            return {
                "task_id": task.task_id,
                "node_id": node.node_id,
                "selection_score": selection_score,
                "selection_score_type": selection_score_type,
                "resource_suitability_score":
                    evaluation_scores[
                        "resource_suitability_score"
                    ],
                "dynamic_qos_score":
                    evaluation_scores[
                        "dynamic_qos_score"
                    ],
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
            "selection_score": selection_score,
            "selection_score_type": selection_score_type,
            "resource_suitability_score":
                evaluation_scores[
                    "resource_suitability_score"
                ],
            "dynamic_qos_score":
                evaluation_scores[
                    "dynamic_qos_score"
                ],
            "execution_time": result["execution_time"],
            "deadline_met": result["deadline_met"],
            "state": result["state"]
        }

    def run_scheduler_variant(
        self,
        scenario_name,
        strategy_name
    ):
        if scenario_name == "deadline_resource_tradeoff":
            nodes = self.create_tradeoff_nodes()
            tasks = self.create_tasks(
                "deadline_resource_tradeoff"
            )
        else:
            conditions = self.get_scenario_conditions(
                scenario_name
            )

            task_profile = self.get_task_profile(
                scenario_name
            )

            nodes = self.create_nodes(
                conditions
            )

            tasks = self.create_tasks(
                task_profile
            )

        if strategy_name == "resource_only":
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
                        selection_score=resource_score,
                        selection_score_type="resource_suitability"
                    )
                )

            return self.build_summary(
                scenario_name,
                strategy_name,
                results
            )

        scheduler = QoSScheduler(
            nodes,
            mode=strategy_name
        )

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
                        selection_score=None,
                        selection_score_type=strategy_name
                    )
                )
                continue

            selected = rankings[0]

            node = selected["node"]
            selection_score = selected["final_score"]

            results.append(
                self.execute_assignment(
                    task=task,
                    node=node,
                    selection_score=selection_score,
                    selection_score_type=strategy_name
                )
            )

        return self.build_summary(
            scenario_name,
            strategy_name,
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

        resource_scores = [
            result["resource_suitability_score"]
            for result in valid_results
            if result["resource_suitability_score"] is not None
        ]

        if resource_scores:
            average_resource_suitability = round(
                sum(resource_scores)
                / len(resource_scores),
                2
            )
        else:
            average_resource_suitability = 0.0

        dynamic_qos_scores = [
            result["dynamic_qos_score"]
            for result in valid_results
            if result["dynamic_qos_score"] is not None
        ]

        if dynamic_qos_scores:
            average_dynamic_qos = round(
                sum(dynamic_qos_scores)
                / len(dynamic_qos_scores),
                2
            )
        else:
            average_dynamic_qos = 0.0

        selection_scores = [
            result["selection_score"]
            for result in valid_results
            if result["selection_score"] is not None
        ]

        if selection_scores:
            average_selection_score = round(
                sum(selection_scores)
                / len(selection_scores),
                2
            )
        else:
            average_selection_score = 0.0

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
            "average_selection_score": average_selection_score,
            "average_resource_suitability":
                average_resource_suitability,
            "average_dynamic_qos":
                average_dynamic_qos,
            "node_usage": node_usage,
            "task_results": results
        }

    def run_scenario(self, scenario_name):
        return {
            strategy: self.run_scheduler_variant(
                scenario_name,
                strategy
            )
            for strategy in self.STRATEGIES
        }

    def run_all_scenarios(self):
        all_results = []

        for scenario_name in self.SCENARIOS:
            scenario_results = self.run_scenario(
                scenario_name
            )

            for strategy_name, result in scenario_results.items():

                task_results = result["task_results"]

                selected_nodes = [
                    task_result["node_id"]
                    for task_result in task_results
                    if task_result["node_id"] is not None
                ]

                selected_node = (
                    ",".join(selected_nodes)
                    if selected_nodes
                    else "None"
                )

                all_results.append({
                    "scenario": scenario_name,
                    "strategy": strategy_name,
                    "selected_node": selected_node,
                    "completed_tasks":
                        result["completed_tasks"],
                    "failed_tasks":
                        result["failed_tasks"],
                    "deadline_success_rate":
                        result["deadline_success_rate"],
                    "average_execution_time":
                        result["average_execution_time"],
                    "average_selection_score":
                        result["average_selection_score"],
                    "average_resource_suitability":
                        result["average_resource_suitability"],
                    "average_dynamic_qos":
                        result["average_dynamic_qos"],
                    "edge_01_usage":
                        result["node_usage"].get(
                            "edge-01",
                            0
                        ),
                    "edge_02_usage":
                        result["node_usage"].get(
                            "edge-02",
                            0
                        ),
                    "cloud_01_usage":
                        result["node_usage"].get(
                            "cloud-01",
                            0
                        )
                })

        return all_results

    def save_results_csv(
        self,
        results,
        filename="ablation_results.csv"
    ):
        output_path = Path("results") / filename

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        fieldnames = [
            "scenario",
            "strategy",
            "selected_node",
            "completed_tasks",
            "failed_tasks",
            "deadline_success_rate",
            "average_execution_time",
            "average_selection_score",
            "average_resource_suitability",
            "average_dynamic_qos",
            "edge_01_usage",
            "edge_02_usage",
            "cloud_01_usage"
        ]

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(results)

        return output_path


if __name__ == "__main__":
    experiment = AblationExperiment()

    print("=" * 100)
    print("DYNAMIC QOS ABLATION EXPERIMENT")
    print("=" * 100)

    all_results = experiment.run_all_scenarios()

    for result in all_results:
        print(
            f"{result['scenario']:<28}"
            f"{result['strategy']:<18}"
            f"Node={result['selected_node']:<12}"
            f"Completed={result['completed_tasks']:<3}"
            f"Failed={result['failed_tasks']:<3}"
            f"Deadline={result['deadline_success_rate']:<6}"
            f"Time={result['average_execution_time']:<6}"
            f"Selection={result['average_selection_score']:<7}"
            f"Resource={result['average_resource_suitability']:<7}"
            f"DynamicQoS={result['average_dynamic_qos']}"
        )

    output_path = experiment.save_results_csv(
        all_results
    )

    print("=" * 100)
    print(
        f"Saved ablation results to: {output_path}"
    )
    print("=" * 100)