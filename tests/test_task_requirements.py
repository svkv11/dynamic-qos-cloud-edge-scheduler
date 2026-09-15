from genai.task_requirements import TaskRequirements


def main():
    print("=" * 60)
    print("TASK REQUIREMENTS TEST")
    print("=" * 60)

    requirements = TaskRequirements(
        workload_type="gpu_intensive",
        cpu_required=4,
        memory_required_gb=8,
        gpu_required=True,
        deadline_seconds=10,
        priority=5
    )

    requirements.display_info()

    data = requirements.to_dict()

    print()
    print("Dictionary Representation")
    print("-" * 60)

    for key, value in data.items():
        print(f"{key}: {value}")

    assert data["workload_type"] == "gpu_intensive"
    assert data["cpu_required"] == 4
    assert data["memory_required_gb"] == 8
    assert data["gpu_required"] is True
    assert data["deadline_seconds"] == 10
    assert data["priority"] == 5

    print()
    print("=" * 60)
    print("TEST RESULT")
    print("=" * 60)
    print("Task Requirements Test: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()