from genai.mock_interpreter import MockRequirementInterpreter
from genai.gemini_interpreter import (
    GeminiRequirementInterpreter
)
from genai.ollama_interpreter import (
    OllamaRequirementInterpreter
)
from genai.task_converter import TaskConverter
from genai.task_validator import TaskRequirementsValidator


class GenAIService:
    """
    Main interface for the GenAI requirement interpretation layer.

    The service can use:
        - MockRequirementInterpreter
        - GeminiRequirementInterpreter
        - OllamaRequirementInterpreter

    The scheduler does not need to know which interpreter
    is being used.
    """

    def __init__(
        self,
        interpreter=None,
        use_gemini=False,
        use_ollama=False
    ):
        if interpreter is not None:
            self.interpreter = interpreter

        elif use_ollama:
            self.interpreter = (
                OllamaRequirementInterpreter()
            )

        elif use_gemini:
            self.interpreter = (
                GeminiRequirementInterpreter()
            )

        else:
            self.interpreter = (
                MockRequirementInterpreter()
            )

    def interpret_request(self, user_request):
        """
        Convert a natural-language request into
        validated TaskRequirements.
        """

        if not isinstance(
            user_request,
            str
        ):
            raise TypeError(
                "user_request must be a string."
            )

        if not user_request.strip():
            raise ValueError(
                "user_request cannot be empty."
            )

        requirements = self.interpreter.interpret(
            user_request
        )

        valid, errors = (
            TaskRequirementsValidator.validate(
                requirements
            )
        )

        if not valid:
            raise ValueError(
                "Invalid task requirements: "
                + "; ".join(errors)
            )

        return requirements

    def create_task(
        self,
        user_request,
        task_id,
        max_retries=3
    ):
        """
        Convert a natural-language request directly
        into a validated scheduler Task.
        """

        requirements = self.interpret_request(
            user_request
        )

        return TaskConverter.requirements_to_task(
            requirements=requirements,
            task_id=task_id,
            max_retries=max_retries
        )