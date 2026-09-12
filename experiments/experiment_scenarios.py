class ExperimentScenarios:
    """
    Define controlled resource and workload conditions
    for scheduler experiments.
    """

    @staticmethod
    def normal():
        return {
            "edge-01": {
                "cpu_utilization": 25.0,
                "memory_utilization": 30.0,
                "gpu_utilization": 0.0,
                "network_latency_ms": 10.0
            },
            "edge-02": {
                "cpu_utilization": 40.0,
                "memory_utilization": 45.0,
                "gpu_utilization": 20.0,
                "network_latency_ms": 15.0
            },
            "cloud-01": {
                "cpu_utilization": 55.0,
                "memory_utilization": 50.0,
                "gpu_utilization": 35.0,
                "network_latency_ms": 80.0
            }
        }

    @staticmethod
    def high_cpu():
        conditions = ExperimentScenarios.normal()

        conditions["edge-02"]["cpu_utilization"] = 85.0

        return conditions

    @staticmethod
    def high_memory():
        conditions = ExperimentScenarios.normal()

        conditions["edge-02"]["memory_utilization"] = 80.0

        return conditions

    @staticmethod
    def high_latency():
        conditions = ExperimentScenarios.normal()

        conditions["edge-02"]["network_latency_ms"] = 50.0

        return conditions

    @staticmethod
    def tight_deadline():
        """
        Return normal node resources for a tight-deadline
        workload experiment.

        Task deadline changes are handled separately by
        the experiment workload configuration.
        """
        return ExperimentScenarios.normal()

    @staticmethod
    def priority_conflict():
        """
        Return normal node resources for a priority-conflict
        workload experiment.

        Task priority changes are handled separately by
        the experiment workload configuration.
        """
        return ExperimentScenarios.normal()

    @staticmethod
    def resource_deadline_pressure():
        """
        Return resource conditions for a combined
        resource and deadline-pressure experiment.
        """

        conditions = ExperimentScenarios.normal()

        conditions["edge-02"]["cpu_utilization"] = 80.0
        conditions["edge-02"]["memory_utilization"] = 75.0
        conditions["edge-02"]["network_latency_ms"] = 45.0

        return conditions

    @staticmethod
    def get_task_profile(scenario_name):
        """
        Return the workload profile associated with
        an experiment scenario.
        """

        profiles = {
            "normal": "normal",
            "high_cpu": "normal",
            "high_memory": "normal",
            "high_latency": "normal",
            "tight_deadline": "tight_deadline",
            "priority_conflict": "priority_conflict",
            "resource_deadline_pressure": "tight_deadline"
        }

        if scenario_name not in profiles:
            raise ValueError(
                f"Unknown scenario: {scenario_name}. "
                f"Available scenarios: {list(profiles.keys())}"
            )

        return profiles[scenario_name]