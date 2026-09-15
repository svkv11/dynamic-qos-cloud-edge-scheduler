from genai.gemini_interpreter import (
    GeminiRequirementInterpreter
)


def main():
    interpreter = GeminiRequirementInterpreter()

    user_request = (
        "Run a GPU image processing task using "
        "8 GB memory and finish within 10 seconds. "
        "This is a critical priority task."
    )

    requirements = interpreter.interpret(
        user_request
    )

    print()
    print("=" * 50)
    print("GEMINI REQUIREMENT INTERPRETER TEST")
    print("=" * 50)

    requirements.display_info()

    print("Gemini Interpreter Test: PASSED")


if __name__ == "__main__":
    main()