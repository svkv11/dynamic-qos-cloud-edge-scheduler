from genai.task_requirements import TaskRequirements


class TaskRequirementsValidator:
    """
    Validate structured task requirements before they
    are passed to the scheduler.
    """

    VALID_WORKLOAD_TYPES = {
        "general",
        "cpu_intensive",
        "memory_intensive",
        "gpu_intensive",
        "latency_sensitive"
    }

    @staticmethod
    def validate(requirements):
        """
        Validate a TaskRequirements object.

        Returns:
            (True, []) when valid
            (False, [errors]) when invalid
        """

        if not isinstance(
            requirements,
            TaskRequirements
        ):
            return False, [
                "Input must be a TaskRequirements object."
            ]

        errors = []

        # Workload type
        if requirements.workload_type not in (
            TaskRequirementsValidator.VALID_WORKLOAD_TYPES
        ):
            errors.append(
                "Invalid workload_type."
            )

        # CPU
        if not isinstance(
            requirements.cpu_required,
            (int, float)
        ):
            errors.append(
                "cpu_required must be a number."
            )
        elif requirements.cpu_required <= 0:
            errors.append(
                "cpu_required must be greater than 0."
            )

        # Memory
        if not isinstance(
            requirements.memory_required_gb,
            (int, float)
        ):
            errors.append(
                "memory_required_gb must be a number."
            )
        elif requirements.memory_required_gb <= 0:
            errors.append(
                "memory_required_gb must be greater than 0."
            )

        # GPU
        if not isinstance(
            requirements.gpu_required,
            bool
        ):
            errors.append(
                "gpu_required must be True or False."
            )

        # Deadline
        if requirements.deadline_seconds is not None:
            if not isinstance(
                requirements.deadline_seconds,
                (int, float)
            ):
                errors.append(
                    "deadline_seconds must be a number or None."
                )
            elif requirements.deadline_seconds <= 0:
                errors.append(
                    "deadline_seconds must be greater than 0."
                )

        # Priority
        if not isinstance(
            requirements.priority,
            int
        ):
            errors.append(
                "priority must be an integer."
            )
        elif not 1 <= requirements.priority <= 5:
            errors.append(
                "priority must be between 1 and 5."
            )

        return len(errors) == 0, errors