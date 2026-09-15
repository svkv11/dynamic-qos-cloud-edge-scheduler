from genai.workload_profiler import WorkloadProfiler


def main():
    print()
    print("=" * 60)
    print("WORKLOAD PROFILER TEST")
    print("=" * 60)

    workload_types = [
        "general",
        "cpu_intensive",
        "memory_intensive",
        "gpu_intensive",
        "latency_sensitive"
    ]

    for workload_type in workload_types:
        profile = WorkloadProfiler.get_profile(
            workload_type
        )

        print()
        print(f"Workload: {workload_type}")
        print(
            f"CPU: {profile['cpu_required']} cores"
        )
        print(
            f"Memory: "
            f"{profile['memory_required_gb']} GB"
        )
        print(
            f"GPU: {profile['gpu_required']}"
        )

    print()
    print("Workload Profiler Test: PASSED")


if __name__ == "__main__":
    main()