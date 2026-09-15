from genai.task_requirements import TaskRequirements
from genai.task_converter import TaskConverter


def main():
    print("=" * 60)
    print("TASK CONVERTER TEST")
    print("=" * 60)

    requirements = TaskRequirements(
        workload_type="gpu_intensive",
        cpu_required=4,
        memory_required_gb=8,
        gpu_required=True,
        deadline_seconds=10,
        priority=5
    )

    task = TaskConverter.requirements_to_task(
        requirements=requirements,
        task_id="genai-task-01",
        max_retries=2
    )

    task.display_info()

    assert task.task_id == "genai-task-01"
    assert task.workload_type == "gpu_intensive"
    assert task.cpu_required == 4
    assert task.memory_required_gb == 8
    assert task.gpu_required is True
    assert task.deadline_seconds == 10
    assert task.priority == 5
    assert task.max_retries == 2
    assert task.state == "PENDING"

    print("=" * 60)
    print("TEST RESULT")
    print("=" * 60)
    print("Task Converter Test: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()