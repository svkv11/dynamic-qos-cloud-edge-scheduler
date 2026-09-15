from genai.mock_interpreter import MockRequirementInterpreter


def main():
    print("=" * 60)
    print("MOCK REQUIREMENT INTERPRETER TEST")
    print("=" * 60)

    interpreter = MockRequirementInterpreter()

    user_request = (
        "Run a GPU image processing task "
        "using 8 GB memory and finish "
        "within 10 seconds. "
        "This is a critical priority task."
    )

    print("User Request:")
    print(user_request)
    print()

    requirements = interpreter.interpret(
        user_request
    )

    requirements.display_info()

    assert requirements.workload_type == "gpu_intensive"
    assert requirements.cpu_required == 4
    assert requirements.memory_required_gb == 8
    assert requirements.gpu_required is True
    assert requirements.deadline_seconds == 10
    assert requirements.priority == 5

    print("=" * 60)
    print("TEST RESULT")
    print("=" * 60)
    print("Mock Requirement Interpreter Test: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()