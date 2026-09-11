import csv
import os


class ExperimentResultExporter:
    """
    Export comparative experiment results to CSV.
    """

    def build_rows(self, comparison):
        """
        Convert comparison results into CSV-ready rows.
        """

        rows = []

        for scenario_name, result in comparison.items():
            rows.append({
                "scenario": scenario_name,
                "completed_tasks": result["completed_tasks"],
                "failed_tasks": result["failed_tasks"],
                "deadline_success_rate": result[
                    "deadline_success_rate"
                ],
                "average_execution_time": result[
                    "average_execution_time"
                ],
                "average_qos_score": result[
                    "average_qos_score"
                ]
            })

        return rows

    def export_csv(self, comparison, file_path):
        """
        Export experiment comparison results to a CSV file.
        """

        rows = self.build_rows(comparison)

        directory = os.path.dirname(file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        fieldnames = [
            "scenario",
            "completed_tasks",
            "failed_tasks",
            "deadline_success_rate",
            "average_execution_time",
            "average_qos_score"
        ]

        with open(
            file_path,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(rows)

        return file_path