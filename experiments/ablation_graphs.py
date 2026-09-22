import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt


class AblationGraphs:
    """
    Generate research figures from Dynamic QoS ablation results.

    The QoS figure uses the common full Dynamic QoS score
    calculated for the selected node of every strategy.

    Selection scores are intentionally not used for the
    cross-strategy QoS comparison because each strategy
    optimizes a different objective.
    """

    STRATEGY_LABELS = {
        "full": "Full Dynamic QoS",
        "no_priority": "No Priority",
        "no_deadline": "No Deadline",
        "resource_only": "Resource Only"
    }

    STRATEGY_ORDER = [
        "full",
        "no_priority",
        "no_deadline",
        "resource_only"
    ]

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.results = self.load_results()

    def load_results(self):
        """
        Load ablation experiment results from CSV.
        """

        results = []

        with open(
            self.csv_path,
            "r",
            encoding="utf-8"
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:
                results.append({
                    "scenario": row["scenario"],
                    "strategy": row["strategy"],
                    "average_execution_time": float(
                        row["average_execution_time"]
                    ),
                    "average_dynamic_qos": float(
                        row["average_dynamic_qos"]
                    ),
                    "average_resource_suitability": float(
                        row["average_resource_suitability"]
                    ),
                    "average_selection_score": float(
                        row["average_selection_score"]
                    ),
                    "deadline_success_rate": float(
                        row["deadline_success_rate"]
                    )
                })

        return results

    def calculate_aggregates(self):
        """
        Calculate average evaluation metrics for each
        strategy across all ablation scenarios.

        The Dynamic QoS value is the common evaluation
        metric and is therefore comparable across all
        strategies.
        """

        grouped_results = defaultdict(list)

        for result in self.results:
            grouped_results[
                result["strategy"]
            ].append(result)

        aggregates = {}

        for strategy in self.STRATEGY_ORDER:

            strategy_results = grouped_results[strategy]

            if not strategy_results:
                continue

            aggregates[strategy] = {
                "average_dynamic_qos": (
                    sum(
                        result["average_dynamic_qos"]
                        for result in strategy_results
                    )
                    / len(strategy_results)
                ),
                "average_execution_time": (
                    sum(
                        result["average_execution_time"]
                        for result in strategy_results
                    )
                    / len(strategy_results)
                ),
                "deadline_success_rate": (
                    sum(
                        result["deadline_success_rate"]
                        for result in strategy_results
                    )
                    / len(strategy_results)
                )
            }

        return aggregates

    def ensure_output_directory(self, output_path):
        """
        Create output directory when required.
        """

        output_directory = os.path.dirname(
            output_path
        )

        if output_directory:
            os.makedirs(
                output_directory,
                exist_ok=True
            )

    def plot_average_qos(self, output_path):
        """
        Generate average Dynamic QoS comparison figure.

        The plotted metric is the common full Dynamic QoS
        evaluation score, not each strategy's internal
        selection score.
        """

        aggregates = self.calculate_aggregates()

        strategies = [
            strategy
            for strategy in self.STRATEGY_ORDER
            if strategy in aggregates
        ]

        labels = [
            self.STRATEGY_LABELS[strategy]
            for strategy in strategies
        ]

        values = [
            aggregates[strategy]["average_dynamic_qos"]
            for strategy in strategies
        ]

        self.ensure_output_directory(
            output_path
        )

        plt.figure(
            figsize=(9, 5)
        )

        plt.bar(
            labels,
            values
        )

        plt.xlabel(
            "Scheduling Strategy"
        )

        plt.ylabel(
            "Average Dynamic QoS Score"
        )

        plt.title(
            "Ablation Study: Average Dynamic QoS Score"
        )

        plt.xticks(
            rotation=15
        )

        plt.ylim(
            0,
            100
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return output_path

    def plot_average_execution_time(
        self,
        output_path
    ):
        """
        Generate average execution time comparison
        figure.
        """

        aggregates = self.calculate_aggregates()

        strategies = [
            strategy
            for strategy in self.STRATEGY_ORDER
            if strategy in aggregates
        ]

        labels = [
            self.STRATEGY_LABELS[strategy]
            for strategy in strategies
        ]

        values = [
            aggregates[strategy][
                "average_execution_time"
            ]
            for strategy in strategies
        ]

        self.ensure_output_directory(
            output_path
        )

        plt.figure(
            figsize=(9, 5)
        )

        plt.bar(
            labels,
            values
        )

        plt.xlabel(
            "Scheduling Strategy"
        )

        plt.ylabel(
            "Average Estimated Execution Time (seconds)"
        )

        plt.title(
            "Ablation Study: Average Estimated Execution Time"
        )

        plt.xticks(
            rotation=15
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return output_path

    def plot_deadline_success_rate(
        self,
        output_path
    ):
        """
        Generate deadline success rate comparison
        figure.
        """

        aggregates = self.calculate_aggregates()

        strategies = [
            strategy
            for strategy in self.STRATEGY_ORDER
            if strategy in aggregates
        ]

        labels = [
            self.STRATEGY_LABELS[strategy]
            for strategy in strategies
        ]

        values = [
            aggregates[strategy][
                "deadline_success_rate"
            ]
            for strategy in strategies
        ]

        self.ensure_output_directory(
            output_path
        )

        plt.figure(
            figsize=(9, 5)
        )

        plt.bar(
            labels,
            values
        )

        plt.xlabel(
            "Scheduling Strategy"
        )

        plt.ylabel(
            "Deadline Success Rate (%)"
        )

        plt.title(
            "Ablation Study: Deadline Success Rate"
        )

        plt.xticks(
            rotation=15
        )

        plt.ylim(
            0,
            100
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return output_path


def main():
    """
    Generate all ablation study figures.
    """

    csv_path = os.path.join(
        "results",
        "ablation_results.csv"
    )

    output_directory = os.path.join(
        "results",
        "ablation_figures"
    )

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    graphs = AblationGraphs(
        csv_path
    )

    qos_path = graphs.plot_average_qos(
        os.path.join(
            output_directory,
            "ablation_qos_comparison.png"
        )
    )

    execution_time_path = (
        graphs.plot_average_execution_time(
            os.path.join(
                output_directory,
                "ablation_execution_time_comparison.png"
            )
        )
    )

    deadline_path = (
        graphs.plot_deadline_success_rate(
            os.path.join(
                output_directory,
                "ablation_deadline_success_comparison.png"
            )
        )
    )

    print("=" * 80)
    print("DYNAMIC QOS ABLATION FIGURES")
    print("=" * 80)

    print(
        f"Saved: {qos_path}"
    )

    print(
        f"Saved: {execution_time_path}"
    )

    print(
        f"Saved: {deadline_path}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()