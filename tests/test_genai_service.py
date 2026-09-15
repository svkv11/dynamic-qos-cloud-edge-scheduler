from genai.genai_service import GenAIService


def main():
    print("=" * 60)
    print("GENAI SERVICE TEST")
    print("=" * 60)

    service = GenAIService()

    user_request = (
        "Run a GPU image processing task "
        "using 8 GB memory and finish "
        "within 10 seconds. "
        "This is a critical priority task."
    )

    print("USER REQUEST")
    print("-" * 60)
    print(user_request)
    print()

    requirements = service.interpret_request(
        user_request
    )

    print("VALIDATED REQUIREMENTS")
    print("-" * 60)

    requirements.display_info()

    task = service.create_task(
        user_request=user_request,
        task_id="genai-service-task-01",
        max_retries=2
    )

    print()
    print("CREATED SCHEDULER TASK")
    print("-" * 60)

    task.display_info()

    assert requirements.workload_type == "gpu_intensive"
    assert requirements.cpu_required == 4
    assert requirements.memory_required_gb == 8
    assert requirements.gpu_required is True
    assert requirements.deadline_seconds == 10
    assert requirements.priority == 5

    assert task.task_id == "genai-service-task-01"
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
    print("GenAI Service Test: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()