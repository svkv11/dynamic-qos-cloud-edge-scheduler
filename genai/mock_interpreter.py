from genai.task_requirements import TaskRequirements


class MockRequirementInterpreter:
    """
    Simulate the requirement interpretation layer.

    This version uses predefined keyword rules instead
    of an actual language model.

    It is kept as a fallback/testing interpreter while
    Gemini is used as the real GenAI interpreter.
    """

    def interpret(self, user_request):
        """
        Convert a natural-language request into
        structured TaskRequirements.
        """

        request = user_request.lower()

        workload_type = "general"
        cpu_required = 2
        memory_required_gb = 4
        gpu_required = False
        deadline_seconds = None
        priority = 3

        if (
            "gpu" in request
            or "image processing" in request
            or "image generation" in request
            or "deep learning" in request
            or "model training" in request
        ):
            workload_type = "gpu_intensive"
            cpu_required = 4
            memory_required_gb = 8
            gpu_required = True

        elif (
            "memory" in request
            or "large dataset" in request
        ):
            workload_type = "memory_intensive"
            cpu_required = 2
            memory_required_gb = 8

        elif (
            "cpu" in request
            or "computation" in request
            or "heavy computation" in request
        ):
            workload_type = "cpu_intensive"
            cpu_required = 4
            memory_required_gb = 4

        elif (
            "low latency" in request
            or "latency sensitive" in request
            or "real time" in request
        ):
            workload_type = "latency_sensitive"
            cpu_required = 1
            memory_required_gb = 2

        if "10 seconds" in request:
            deadline_seconds = 10

        elif "20 seconds" in request:
            deadline_seconds = 20

        elif "30 seconds" in request:
            deadline_seconds = 30

        if (
            "critical" in request
            or "highest priority" in request
            or "urgent" in request
        ):
            priority = 5

        elif "high priority" in request:
            priority = 4

        elif "low priority" in request:
            priority = 1

        return TaskRequirements(
            workload_type=workload_type,
            cpu_required=cpu_required,
            memory_required_gb=memory_required_gb,
            gpu_required=gpu_required,
            deadline_seconds=deadline_seconds,
            priority=priority
        )