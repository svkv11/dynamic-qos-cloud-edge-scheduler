from workload_profiler import WorkloadProfiler


print("=" * 60)
print("WORKLOAD PROFILER TEST")
print("=" * 60)


test_cases = [
    {
        "workload_type": "gpu_intensive",
        "gpu_required": True,
        "priority": 5,
        "deadline_seconds": 20,
        "explicit_cpu_required": 10,
        "explicit_memory_required_gb": 16
    },
    {
        "workload_type": "memory_intensive",
        "gpu_required": False,
        "priority": 3,
        "deadline_seconds": None,
        "explicit_cpu_required": None,
        "explicit_memory_required_gb": 100
    },
    {
        "workload_type": "cpu_intensive",
        "gpu_required": False,
        "priority": 5,
        "deadline_seconds": None,
        "explicit_cpu_required": 100,
        "explicit_memory_required_gb": 16
    },
    {
        "workload_type": "normal",
        "gpu_required": False,
        "priority": 3,
        "deadline_seconds": None,
        "explicit_cpu_required": None,
        "explicit_memory_required_gb": None
    }
]


for index, test_case in enumerate(test_cases, start=1):

    print(f"\nTest Case {index}")
    print("-" * 40)

    print("Input:")
    print(test_case)

    result = WorkloadProfiler.build_requirements(
        test_case
    )

    print("\nProfiled Requirements:")
    print(result)


print("\n" + "=" * 60)
print("PROFILER TEST COMPLETED")
print("=" * 60)