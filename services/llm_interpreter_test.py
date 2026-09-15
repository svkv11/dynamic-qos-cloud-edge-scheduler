from llm_requirement_interpreter import (
    LLMRequirementInterpreter
)


print("=" * 60)
print("LLM REQUIREMENT INTERPRETER TEST")
print("=" * 60)


test_requests = [
    "Create an AI image quickly.",
    "Run my model using 8 CPU cores and 16 GB RAM within 20 seconds.",
    "Analyze a very large dataset that requires a lot of RAM."
]


for index, user_request in enumerate(test_requests, start=1):

    print(f"\nTest Case {index}")
    print("-" * 40)

    print("User Request:")
    print(user_request)

    try:
        requirements = (
            LLMRequirementInterpreter.interpret(
                user_request
            )
        )

        print("\nInterpreted Requirements:")
        print(requirements)

    except Exception as error:
        print("\nERROR:")
        print(error)


print("\n" + "=" * 60)
print("LLM INTERPRETER TEST COMPLETED")
print("=" * 60)