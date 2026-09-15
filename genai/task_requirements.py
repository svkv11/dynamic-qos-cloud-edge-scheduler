class TaskRequirements:
    """
    Structured task requirements produced by the
    GenAI requirement interpretation layer.

    This class acts as the interface between:
        Natural-language user requirements
        and
        the existing Task model.
    """

    def __init__(
        self,
        workload_type,
        cpu_required,
        memory_required_gb,
        gpu_required=False,
        deadline_seconds=None,
        priority=1
    ):
        self.workload_type = workload_type
        self.cpu_required = cpu_required
        self.memory_required_gb = memory_required_gb
        self.gpu_required = gpu_required
        self.deadline_seconds = deadline_seconds
        self.priority = priority

    def to_dict(self):
        """
        Convert the structured requirements into
        a dictionary representation.
        """

        return {
            "workload_type": self.workload_type,
            "cpu_required": self.cpu_required,
            "memory_required_gb": self.memory_required_gb,
            "gpu_required": self.gpu_required,
            "deadline_seconds": self.deadline_seconds,
            "priority": self.priority
        }

    def display_info(self):
        """
        Display the interpreted task requirements.
        """

        print("=" * 50)
        print("TASK REQUIREMENTS")
        print("=" * 50)

        print(
            f"Workload Type: "
            f"{self.workload_type}"
        )

        print(
            f"CPU Required: "
            f"{self.cpu_required} cores"
        )

        print(
            f"Memory Required: "
            f"{self.memory_required_gb} GB"
        )

        print(
            f"GPU Required: "
            f"{self.gpu_required}"
        )

        print(
            f"Deadline: "
            f"{self.deadline_seconds} seconds"
        )

        print(
            f"Priority: "
            f"{self.priority}"
        )

        print("=" * 50)