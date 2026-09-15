class MetricsCollector:

    def __init__(self):
        self.records = []

    def record_task(
        self,
        task,
        node,
        execution_time,
        deadline_met,
        qos_score=None
    ):
        """
        Record the result of a completed or failed task.
        """

        record = {
            "task_id": task.task_id,
            "workload_type": task.workload_type,
            "node_id": node.node_id,
            "node_type": node.node_type,
            "execution_time": execution_time,
            "deadline_seconds": task.deadline_seconds,
            "deadline_met": deadline_met,
            "priority": task.priority,
            "qos_score": qos_score,
            "state": task.state
        }

        self.records.append(record)

        return record

    def get_records(self):
        return self.records

    def get_total_tasks(self):
        return len(self.records)

    def get_completed_tasks(self):
        return sum(
            1
            for record in self.records
            if record["state"] == "COMPLETED"
        )

    def get_failed_tasks(self):
        return sum(
            1
            for record in self.records
            if record["state"] == "FAILED"
        )

    def get_deadline_success_rate(self):
        if not self.records:
            return 0.0

        deadline_results = [
            record
            for record in self.records
            if record["deadline_met"] is not None
        ]

        if not deadline_results:
            return 0.0

        successful = sum(
            1
            for record in deadline_results
            if record["deadline_met"]
        )

        return round(
            (successful / len(deadline_results)) * 100,
            2
        )

    def get_average_execution_time(self):
        if not self.records:
            return 0.0

        total_time = sum(
            record["execution_time"]
            for record in self.records
        )

        return round(
            total_time / len(self.records),
            2
        )

    def get_average_qos_score(self):
        qos_records = [
            record
            for record in self.records
            if record["qos_score"] is not None
        ]

        if not qos_records:
            return 0.0

        total_qos = sum(
            record["qos_score"]
            for record in qos_records
        )

        return round(
            total_qos / len(qos_records),
            2
        )

    def get_node_usage(self):
        usage = {}

        for record in self.records:
            node_id = record["node_id"]

            if node_id not in usage:
                usage[node_id] = 0

            usage[node_id] += 1

        return usage

    def display_summary(self):
        print("=" * 60)
        print("SCHEDULER METRICS SUMMARY")
        print("=" * 60)

        print(
            f"Total Tasks: "
            f"{self.get_total_tasks()}"
        )

        print(
            f"Completed Tasks: "
            f"{self.get_completed_tasks()}"
        )

        print(
            f"Failed Tasks: "
            f"{self.get_failed_tasks()}"
        )

        print(
            f"Deadline Success Rate: "
            f"{self.get_deadline_success_rate()}%"
        )

        print(
            f"Average Execution Time: "
            f"{self.get_average_execution_time()} seconds"
        )

        print(
            f"Average QoS Score: "
            f"{self.get_average_qos_score()}"
        )

        print("Node Usage:")

        node_usage = self.get_node_usage()

        if not node_usage:
            print("  No task records.")

        else:
            for node_id, count in node_usage.items():
                print(
                    f"  {node_id}: "
                    f"{count} task(s)"
                )

        print("=" * 60)