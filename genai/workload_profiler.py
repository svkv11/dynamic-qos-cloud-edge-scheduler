class WorkloadProfiler:
    """
    Convert workload characteristics into infrastructure
    requirements.

    The profiler provides defaults for resources that the
    user did not explicitly specify.
    """

    PROFILES = {
        "general": {
            "cpu_required": 2,
            "memory_required_gb": 4,
            "gpu_required": False
        },

        "cpu_intensive": {
            "cpu_required": 4,
            "memory_required_gb": 4,
            "gpu_required": False
        },

        "memory_intensive": {
            "cpu_required": 2,
            "memory_required_gb": 8,
            "gpu_required": False
        },

        "gpu_intensive": {
            "cpu_required": 4,
            "memory_required_gb": 8,
            "gpu_required": True
        },

        "latency_sensitive": {
            "cpu_required": 1,
            "memory_required_gb": 2,
            "gpu_required": False
        }
    }

    @classmethod
    def get_profile(cls, workload_type):
        """
        Return the default infrastructure profile.
        """

        if workload_type not in cls.PROFILES:
            raise ValueError(
                f"Unknown workload type: {workload_type}"
            )

        return cls.PROFILES[workload_type].copy()

    @classmethod
    def apply_profile(
        cls,
        requirements,
        cpu_explicit=False,
        memory_explicit=False,
        gpu_explicit=False
    ):
        """
        Apply workload defaults while preserving
        explicitly provided resource requirements.
        """

        profile = cls.get_profile(
            requirements.workload_type
        )

        if not cpu_explicit:
            requirements.cpu_required = profile[
                "cpu_required"
            ]

        if not memory_explicit:
            requirements.memory_required_gb = profile[
                "memory_required_gb"
            ]

        if not gpu_explicit:
            requirements.gpu_required = profile[
                "gpu_required"
            ]

        return requirements