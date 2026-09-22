class ExecutionResult:
    """
    Store the result of a real workload execution.

    This class belongs to the Live Execution Layer.
    It is intentionally separate from the research
    execution-time estimation used by the scheduler.
    """

    def __init__(
        self,
        task_id,
        node_id,
        workload_type,
        output,
        actual_execution_time,
        deadline_seconds=None,
        deadline_met=None,
        success=True,
        error=None
    ):
        self.task_id = task_id
        self.node_id = node_id
        self.workload_type = workload_type
        self.output = output
        self.actual_execution_time = actual_execution_time
        self.deadline_seconds = deadline_seconds
        self.deadline_met = deadline_met
        self.success = success
        self.error = error

    def to_dict(self):
        """
        Convert the execution result into a dictionary.
        """
        return {
            "task_id": self.task_id,
            "node_id": self.node_id,
            "workload_type": self.workload_type,
            "output": self.output,
            "actual_execution_time": self.actual_execution_time,
            "deadline_seconds": self.deadline_seconds,
            "deadline_met": self.deadline_met,
            "success": self.success,
            "error": self.error
        }

    def display(self):
        """
        Display the live execution result.
        """
        print()
        print("=" * 60)
        print("LIVE EXECUTION RESULT")
        print("=" * 60)

        print(f"Task ID: {self.task_id}")
        print(f"Selected Node: {self.node_id}")
        print(f"Workload Type: {self.workload_type}")
        print(
            f"Actual Execution Time: "
            f"{self.actual_execution_time} seconds"
        )

        print(
            f"Deadline: "
            f"{self.deadline_seconds} seconds"
        )

        if self.deadline_met is True:
            print("Deadline Status: MET")
        elif self.deadline_met is False:
            print("Deadline Status: MISSED")
        else:
            print("Deadline Status: NOT SPECIFIED")

        print(
            f"Execution Status: "
            f"{'SUCCESS' if self.success else 'FAILED'}"
        )

        if self.error is not None:
            print(f"Error: {self.error}")

        print()
        print("OUTPUT")
        print("-" * 60)
        print(self.output)
        print("-" * 60)