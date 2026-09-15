class WorkloadProfiler:
    """
    Converts interpreted natural-language requirements into
    concrete resource requirements for the scheduler.
    """

    DEFAULT_PROFILES = {
        "normal": {
            "cpu_required": 2,
            "memory_required_gb": 4,
            "gpu_required": False
        },
        "cpu_intensive": {
            "cpu_required": 4,
            "memory_required_gb": 8,
            "gpu_required": False
        },
        "memory_intensive": {
            "cpu_required": 4,
            "memory_required_gb": 12,
            "gpu_required": False
        },
        "gpu_intensive": {
            "cpu_required": 4,
            "memory_required_gb": 8,
            "gpu_required": True
        }
    }

    @classmethod
    def get_profile(cls, workload_type):
        """
        Return the default resource profile for a workload type.
        """

        profile = cls.DEFAULT_PROFILES.get(
            workload_type,
            cls.DEFAULT_PROFILES["normal"]
        )

        return profile.copy()

    @classmethod
    def build_requirements(cls, interpreted_requirements):
        """
        Convert LLM-interpreted requirements into the final
        technical requirements used by the scheduler.

        Explicit CPU and memory values provided by the user
        take priority over default workload profiles.

        If the user did not provide CPU or memory,
        the profiler uses the workload's default profile.
        """

        workload_type = interpreted_requirements.get(
            "workload_type",
            "normal"
        )

        profile = cls.get_profile(workload_type)

        # --------------------------------------------------
        # CPU
        # --------------------------------------------------

        explicit_cpu = interpreted_requirements.get(
            "explicit_cpu_required"
        )

        if isinstance(explicit_cpu, (int, float)) and explicit_cpu > 0:
            cpu_required = explicit_cpu
        else:
            cpu_required = profile["cpu_required"]

        # --------------------------------------------------
        # Memory
        # --------------------------------------------------

        explicit_memory = interpreted_requirements.get(
            "explicit_memory_required_gb"
        )

        if (
            isinstance(explicit_memory, (int, float))
            and explicit_memory > 0
        ):
            memory_required_gb = explicit_memory
        else:
            memory_required_gb = profile["memory_required_gb"]

        # --------------------------------------------------
        # GPU
        # --------------------------------------------------

        gpu_required = interpreted_requirements.get(
            "gpu_required"
        )

        if gpu_required is None:
            gpu_required = profile["gpu_required"]
        else:
            gpu_required = bool(gpu_required)

        # --------------------------------------------------
        # Priority
        # --------------------------------------------------

        priority = interpreted_requirements.get(
            "priority",
            3
        )

        if not isinstance(priority, int):
            priority = 3

        if priority < 1:
            priority = 1

        if priority > 5:
            priority = 5

        # --------------------------------------------------
        # Deadline
        # --------------------------------------------------

        deadline_seconds = interpreted_requirements.get(
            "deadline_seconds"
        )

        if not isinstance(deadline_seconds, (int, float)):
            deadline_seconds = None

        # --------------------------------------------------
        # Final requirements
        # --------------------------------------------------

        return {
            "workload_type": workload_type,
            "cpu_required": cpu_required,
            "memory_required_gb": memory_required_gb,
            "gpu_required": gpu_required,
            "priority": priority,
            "deadline_seconds": deadline_seconds
        }