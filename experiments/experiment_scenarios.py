class ExperimentScenarios:
    """
    Define controlled resource conditions for experiments.
    """

    @staticmethod
    def normal():
        """
        Return the standard resource conditions.
        """

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
        """
        Simulate high CPU utilization on edge-02.
        """

        conditions = ExperimentScenarios.normal()

        conditions["edge-02"]["cpu_utilization"] = 85.0

        return conditions

    @staticmethod
    def high_memory():
        """
        Simulate high memory utilization on edge-02.
        """

        conditions = ExperimentScenarios.normal()

        conditions["edge-02"]["memory_utilization"] = 80.0

        return conditions

    @staticmethod
    def high_latency():
        """
        Simulate high network latency on edge-02.
        """

        conditions = ExperimentScenarios.normal()

        conditions["edge-02"]["network_latency_ms"] = 50.0

        return conditions