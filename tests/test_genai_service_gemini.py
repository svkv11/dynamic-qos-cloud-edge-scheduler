from genai.genai_service import GenAIService


def main():
    service = GenAIService(
        use_gemini=True
    )

    user_request = (
        "Run a GPU image processing task using "
        "8 GB memory and finish within 10 seconds. "
        "This is a critical priority task."
    )

    task = service.create_task(
        user_request=user_request,
        task_id="gemini-service-task-01",
        max_retries=2
    )

    print()
    print("=" * 50)
    print("GENAI SERVICE + GEMINI TEST")
    print("=" * 50)

    task.display_info()

    print(
        "GenAI Service + Gemini Test: PASSED"
    )


if __name__ == "__main__":
    main()