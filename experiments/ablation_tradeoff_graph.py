import csv
import os

import matplotlib.pyplot as plt


class AblationTradeoffGraph:
    """
    Generate a focused figure for the
    deadline-resource trade-off scenario.
    """

    STRATEGY_ORDER = [
        "full",
        "no_priority",
        "no_deadline",
        "resource_only"
    ]

    STRATEGY_LABELS = {
        "full": "Full Dynamic QoS",
        "no_priority": "No Priority",
        "no_deadline": "No Deadline",
        "resource_only": "Resource Only"
    }

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def load_tradeoff_results(self):
        """
        Load only the deadline-resource trade-off scenario.
        """

        results = []

        with open(
            self.csv_path,
            "r",
            encoding="utf-8"
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:

                if row["scenario"] != "deadline_resource_tradeoff":
                    continue

                results.append({
                    "strategy": row["strategy"],
                    "selected_node": row["selected_node"],
                    "average_execution_time": float(
                        row["average_execution_time"]
                    ),
                    "deadline_success_rate": float(
                        row["deadline_success_rate"]
                    )
                })

        return results

    def get_ordered_results(self):
        """
        Arrange results according to the defined strategy order.
        """

        results = self.load_tradeoff_results()

        result_map = {
            result["strategy"]: result
            for result in results
        }

        return [
            result_map[strategy]
            for strategy in self.STRATEGY_ORDER
            if strategy in result_map
        ]

    def generate(self, output_path):
        """
        Generate the trade-off figure.
        """

        results = self.get_ordered_results()

        labels = [
            self.STRATEGY_LABELS[result["strategy"]]
            for result in results
        ]

        execution_times = [
            result["average_execution_time"]
            for result in results
        ]

        deadline_rates = [
            result["deadline_success_rate"]
            for result in results
        ]

        selected_nodes = [
            result["selected_node"]
            for result in results
        ]

        output_directory = os.path.dirname(output_path)

        if output_directory:
            os.makedirs(
                output_directory,
                exist_ok=True
            )

        positions = list(range(len(labels)))

        figure, axis = plt.subplots(
            figsize=(10, 6)
        )

        bars = axis.bar(
            positions,
            execution_times,
            width=0.6
        )

        axis.set_xlabel(
            "Scheduling Strategy"
        )

        axis.set_ylabel(
            "Execution Time (seconds)"
        )

        axis.set_title(
            "Deadline-Resource Trade-off Scenario"
        )

        axis.set_xticks(
            positions
        )

        axis.set_xticklabels(
            labels,
            rotation=15
        )

        axis.set_ylim(
            0,
            max(execution_times) + 3
        )

        for bar, node, deadline_rate in zip(
            bars,
            selected_nodes,
            deadline_rates
        ):

            axis.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.2,
                f"{node}\nDeadline: {deadline_rate:.0f}%",
                ha="center",
                va="bottom",
                fontsize=9
            )

        axis.axhline(
            y=10,
            linestyle="--",
            linewidth=1.5,
            label="Deadline = 10 seconds"
        )

        axis.legend()

        figure.tight_layout()

        figure.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close(figure)

        return output_path


def main():
    """
    Generate the deadline-resource trade-off figure.
    """

    csv_path = os.path.join(
        "results",
        "ablation_results.csv"
    )

    output_path = os.path.join(
        "results",
        "ablation_figures",
        "deadline_resource_tradeoff.png"
    )

    graph = AblationTradeoffGraph(
        csv_path
    )

    saved_path = graph.generate(
        output_path
    )

    print("=" * 80)
    print("DEADLINE-RESOURCE TRADE-OFF FIGURE")
    print("=" * 80)

    print(
        f"Saved: {saved_path}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()