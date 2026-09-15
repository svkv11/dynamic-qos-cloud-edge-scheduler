from llm_requirement_interpreter import (
    LLMRequirementInterpreter
)

from workload_profiler import (
    WorkloadProfiler
)


print("=" * 60)
print("LLM + WORKLOAD PROFILER INTEGRATION TEST")
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

        # -----------------------------------------------
        # Step 1: Interpret natural-language request
        # -----------------------------------------------

        interpreted_requirements = (
            LLMRequirementInterpreter.interpret(
                user_request
            )
        )

        print("\nLLM Interpretation:")
        print(interpreted_requirements)

        # -----------------------------------------------
        # Step 2: Build final technical requirements
        # -----------------------------------------------

        final_requirements = (
            WorkloadProfiler.build_requirements(
                interpreted_requirements
            )
        )

        print("\nFinal Profiled Requirements:")
        print(final_requirements)

    except Exception as error:

        print("\nERROR:")
        print(error)


print("\n" + "=" * 60)
print("INTEGRATION TEST COMPLETED")
print("=" * 60)