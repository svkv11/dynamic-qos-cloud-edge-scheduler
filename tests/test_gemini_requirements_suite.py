from genai.gemini_interpreter import (
    GeminiRequirementInterpreter
)


def main():
    interpreter = GeminiRequirementInterpreter()

    test_cases = [
        {
            "name": "GPU Task",
            "request": (
                "Run a deep learning image processing task "
                "using 8 GB memory with a GPU. "
                "Finish within 10 seconds. "
                "This is a critical priority task."
            ),
            "expected": {
                "workload_type": "gpu_intensive",
                "cpu_required": 4,
                "memory_required_gb": 8,
                "gpu_required": True,
                "deadline_seconds": 10,
                "priority": 5
            }
        },
        {
            "name": "CPU Task",
            "request": (
                "Run a CPU intensive computation task "
                "using 6 CPU cores and 16 GB memory. "
                "This is a high priority task."
            ),
            "expected": {
                "workload_type": "cpu_intensive",
                "cpu_required": 6,
                "memory_required_gb": 16,
                "gpu_required": False,
                "deadline_seconds": None,
                "priority": 4
            }
        },
        {
            "name": "Memory Task",
            "request": (
                "Process a large dataset that needs "
                "12 GB of memory. It is a medium priority task."
            ),
            "expected": {
                "workload_type": "memory_intensive",
                "cpu_required": 2,
                "memory_required_gb": 12,
                "gpu_required": False,
                "deadline_seconds": None,
                "priority": 3
            }
        },
        {
            "name": "Latency Task",
            "request": (
                "Run a real time application that is "
                "latency sensitive and must finish within "
                "20 seconds. This is a high priority task."
            ),
            "expected": {
                "workload_type": "latency_sensitive",
                "cpu_required": 1,
                "memory_required_gb": 2,
                "gpu_required": False,
                "deadline_seconds": 20,
                "priority": 4
            }
        },
        {
            "name": "General Task",
            "request": (
                "Run a normal general purpose task."
            ),
            "expected": {
                "workload_type": "general",
                "cpu_required": 2,
                "memory_required_gb": 4,
                "gpu_required": False,
                "deadline_seconds": None,
                "priority": 3
            }
        }
    ]

    print()
    print("=" * 70)
    print("GEMINI REQUIREMENT INTERPRETATION TEST SUITE")
    print("=" * 70)

    passed = 0

    for index, test_case in enumerate(
        test_cases,
        start=1
    ):
        print()
        print(
            f"TEST {index}: {test_case['name']}"
        )
        print("-" * 70)
        print(
            f"Request: {test_case['request']}"
        )

        requirements = interpreter.interpret(
            test_case["request"]
        )

        actual = requirements.to_dict()
        expected = test_case["expected"]

        print()
        print("Gemini output:")

        for key, value in actual.items():
            print(
                f"  {key}: {value}"
            )

        if actual != expected:
            print()
            print("FAILED")
            print("Expected:")
            print(expected)
            print("Actual:")
            print(actual)

            raise AssertionError(
                f"{test_case['name']} failed."
            )

        print("PASSED")
        passed += 1

    print()
    print("=" * 70)
    print(
        f"RESULT: {passed}/{len(test_cases)} TESTS PASSED"
    )
    print("=" * 70)

    print(
        "Gemini Requirement Test Suite: PASSED"
    )


if __name__ == "__main__":
    main()