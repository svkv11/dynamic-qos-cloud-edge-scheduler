from genai.task_requirements import TaskRequirements
from genai.task_validator import TaskRequirementsValidator


def main():
    print("=" * 60)
    print("TASK REQUIREMENTS VALIDATOR TEST")
    print("=" * 60)

    # ---------------------------------------------------------
    # Valid requirements
    # ---------------------------------------------------------

    valid_requirements = TaskRequirements(
        workload_type="gpu_intensive",
        cpu_required=4,
        memory_required_gb=8,
        gpu_required=True,
        deadline_seconds=10,
        priority=5
    )

    valid, errors = (
        TaskRequirementsValidator.validate(
            valid_requirements
        )
    )

    print("VALID REQUIREMENTS")
    print("-" * 60)
    print(f"Valid: {valid}")
    print(f"Errors: {errors}")

    assert valid is True
    assert errors == []

    # ---------------------------------------------------------
    # Invalid requirements
    # ---------------------------------------------------------

    invalid_requirements = TaskRequirements(
        workload_type="unknown_workload",
        cpu_required=-4,
        memory_required_gb=0,
        gpu_required="yes",
        deadline_seconds=-10,
        priority=10
    )

    valid, errors = (
        TaskRequirementsValidator.validate(
            invalid_requirements
        )
    )

    print()
    print("INVALID REQUIREMENTS")
    print("-" * 60)
    print(f"Valid: {valid}")

    for error in errors:
        print(f"- {error}")

    assert valid is False
    assert len(errors) == 6

    print()
    print("=" * 60)
    print("TEST RESULT")
    print("=" * 60)
    print("Task Requirements Validator Test: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()