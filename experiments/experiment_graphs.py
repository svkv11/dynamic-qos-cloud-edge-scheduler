import csv
import os

import matplotlib.pyplot as plt


class ExperimentGraphs:
    """
    Generate graphs from exported experiment results.
    """

    def load_results(self, csv_path):
        """
        Load experiment results from a CSV file.
        """

        results = []

        with open(
            csv_path,
            "r",
            encoding="utf-8"
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:
                results.append({
                    "scenario": row["scenario"],
                    "average_execution_time": float(
                        row["average_execution_time"]
                    ),
                    "average_qos_score": float(
                        row["average_qos_score"]
                    )
                })

        return results

    def plot_average_qos(
        self,
        csv_path,
        output_path
    ):
        """
        Generate an average QoS score comparison chart.
        """

        results = self.load_results(csv_path)

        scenarios = [
            result["scenario"]
            for result in results
        ]

        qos_scores = [
            result["average_qos_score"]
            for result in results
        ]

        output_directory = os.path.dirname(
            output_path
        )

        if output_directory:
            os.makedirs(
                output_directory,
                exist_ok=True
            )

        plt.figure(figsize=(8, 5))

        plt.bar(
            scenarios,
            qos_scores
        )

        plt.xlabel("Scenario")
        plt.ylabel("Average QoS Score")
        plt.title(
            "Average QoS Score Across Experiment Scenarios"
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300
        )

        plt.close()

        return output_path

    def plot_average_execution_time(
        self,
        csv_path,
        output_path
    ):
        """
        Generate an average execution time comparison chart.
        """

        results = self.load_results(csv_path)

        scenarios = [
            result["scenario"]
            for result in results
        ]

        execution_times = [
            result["average_execution_time"]
            for result in results
        ]

        output_directory = os.path.dirname(
            output_path
        )

        if output_directory:
            os.makedirs(
                output_directory,
                exist_ok=True
            )

        plt.figure(figsize=(8, 5))

        plt.bar(
            scenarios,
            execution_times
        )

        plt.xlabel("Scenario")
        plt.ylabel("Average Execution Time (seconds)")
        plt.title(
            "Average Execution Time Across Experiment Scenarios"
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300
        )

        plt.close()

        return output_path