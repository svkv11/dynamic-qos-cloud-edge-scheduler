from experiments.experiment_runner import ExperimentRunner


class ExperimentEvaluator:
    """
    Run and compare multiple scheduler experiments.
    """

    def __init__(self):
        self.runner = ExperimentRunner()

    def get_scenario_names(self):
        """
        Return all predefined experiment scenarios.
        """

        return [
            "normal",
            "high_cpu",
            "high_memory",
            "high_latency",
            "tight_deadline",
            "priority_conflict",
            "resource_deadline_pressure"
        ]

    def run_all_scenarios(self):
        """
        Run all predefined experiment scenarios.
        """

        scenario_names = self.get_scenario_names()

        results = {}

        for scenario_name in scenario_names:
            results[scenario_name] = (
                self.runner.run_experiment(
                    scenario_name
                )
            )

        return results

    def build_comparison(self, results):
        """
        Convert experiment results into a compact
        comparative structure.
        """

        comparison = {}

        for scenario_name, result in results.items():

            comparison[scenario_name] = {
                "completed_tasks": result[
                    "completed_tasks"
                ],
                "failed_tasks": result[
                    "failed_tasks"
                ],
                "deadline_success_rate": result[
                    "deadline_success_rate"
                ],
                "average_execution_time": result[
                    "average_execution_time"
                ],
                "average_qos_score": result[
                    "average_qos_score"
                ],
                "node_usage": result[
                    "node_usage"
                ]
            }

        return comparison

    def get_best_qos_scenario(self, comparison):
        """
        Return the scenario with the highest
        average QoS score.
        """

        return max(
            comparison.items(),
            key=lambda item: item[1][
                "average_qos_score"
            ]
        )[0]

    def get_fastest_scenario(self, comparison):
        """
        Return the scenario with the lowest
        average execution time.
        """

        return min(
            comparison.items(),
            key=lambda item: item[1][
                "average_execution_time"
            ]
        )[0]

    def display_comparison(self, comparison):
        """
        Display a readable comparison of all scenarios.
        """

        print("=" * 90)
        print("SCHEDULER EXPERIMENT COMPARISON")
        print("=" * 90)

        print(
            f"{'Scenario':<30}"
            f"{'Completed':<12}"
            f"{'Failed':<10}"
            f"{'Deadline %':<13}"
            f"{'Avg Time':<12}"
            f"{'Avg QoS':<10}"
        )

        print("-" * 90)

        for scenario_name, result in comparison.items():

            print(
                f"{scenario_name:<30}"
                f"{result['completed_tasks']:<12}"
                f"{result['failed_tasks']:<10}"
                f"{result['deadline_success_rate']:<13}"
                f"{result['average_execution_time']:<12}"
                f"{result['average_qos_score']:<10}"
            )

        print("=" * 90)

        print(
            f"Best QoS Scenario: "
            f"{self.get_best_qos_scenario(comparison)}"
        )

        print(
            f"Fastest Scenario: "
            f"{self.get_fastest_scenario(comparison)}"
        )

        print("=" * 90)