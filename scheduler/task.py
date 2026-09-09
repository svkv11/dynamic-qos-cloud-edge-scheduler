class Task:
    def __init__(
        self,
        task_id,
        workload_type,
        cpu_required,
        memory_required_gb,
        gpu_required=False,
        deadline_seconds=None,
        priority=1,
        max_retries=3
    ):
        self.task_id = task_id
        self.workload_type = workload_type

        # Resource requirements
        self.cpu_required = cpu_required
        self.memory_required_gb = memory_required_gb
        self.gpu_required = gpu_required

        # QoS requirements
        self.deadline_seconds = deadline_seconds
        self.priority = priority

        # Retry configuration
        self.max_retries = max(0, max_retries)
        self.retry_count = 0

        # Task lifecycle
        self.state = "PENDING"

        # Node assigned to the task
        self.assigned_node = None

        # Failure information
        self.failure_reason = None

    def start(self, node):
        """
        Move the task from PENDING to RUNNING.
        """

        self.state = "RUNNING"
        self.assigned_node = node
        self.failure_reason = None

    def complete(self):
        """
        Move the task from RUNNING to COMPLETED.
        """

        self.state = "COMPLETED"

    def fail(self, reason):
        """
        Move the task to FAILED and record the reason.
        """

        self.state = "FAILED"
        self.failure_reason = reason

    def increment_retry(self):
        """
        Increment the number of scheduling or execution retries.
        """

        self.retry_count += 1

    def can_retry(self):
        """
        Check whether the task can be retried.

        Returns True while the retry limit has not
        been reached.
        """

        return self.retry_count < self.max_retries

    def retry(self):
        """
        Move a failed task back to PENDING for another attempt.

        Returns True if the retry is allowed.
        Returns False if the retry limit has been reached.
        """

        if not self.can_retry():
            return False

        self.increment_retry()

        self.state = "PENDING"
        self.assigned_node = None
        self.failure_reason = None

        return True

    def display_info(self):
        print(f"Task ID: {self.task_id}")
        print(f"Workload Type: {self.workload_type}")

        print(f"CPU Required: {self.cpu_required} cores")
        print(f"Memory Required: {self.memory_required_gb} GB")
        print(f"GPU Required: {self.gpu_required}")

        print(f"Deadline: {self.deadline_seconds} seconds")
        print(f"Priority: {self.priority}")

        print(f"Retry Count: {self.retry_count}")
        print(f"Max Retries: {self.max_retries}")

        print(f"State: {self.state}")

        if self.assigned_node is not None:
            print(
                f"Assigned Node: "
                f"{self.assigned_node.node_id}"
            )
        else:
            print("Assigned Node: None")

        if self.failure_reason is not None:
            print(
                f"Failure Reason: "
                f"{self.failure_reason}"
            )
        else:
            print("Failure Reason: None")

        print("-" * 40)