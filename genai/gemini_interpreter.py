
import json
import os

from google import genai

from genai.task_requirements import TaskRequirements
from genai.workload_profiler import WorkloadProfiler


class GeminiRequirementInterpreter:
    """
    Use Gemini structured output to convert a natural-language
    task request into TaskRequirements.

    Gemini identifies the user's intent and workload
    characteristics.

    WorkloadProfiler provides infrastructure defaults for
    requirements that the user did not explicitly specify.
    """

    def __init__(self, model="gemini-3.7-flash"):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = model

    def interpret(self, user_request):
        """
        Convert a natural-language request into
        TaskRequirements using Gemini structured output.
        """

        if not isinstance(user_request, str):
            raise TypeError(
                "user_request must be a string."
            )

        if not user_request.strip():
            raise ValueError(
                "user_request cannot be empty."
            )

        prompt = f"""
You are the requirement interpretation component
of a Dynamic QoS Cloud-Edge Scheduler.

The user should be able to describe their task in
normal natural language without knowing technical
infrastructure requirements.

Your job is to identify:

1. What type of workload the user wants to run.
2. Any CPU requirement explicitly stated by the user.
3. Any memory requirement explicitly stated by the user.
4. Any GPU requirement explicitly stated by the user.
5. Any explicit deadline.
6. The priority or urgency expressed by the user.

Allowed workload types:

- general
- cpu_intensive
- memory_intensive
- gpu_intensive
- latency_sensitive

Workload classification examples:

- image generation -> gpu_intensive
- image processing -> gpu_intensive
- deep learning -> gpu_intensive
- model training -> gpu_intensive
- heavy computation -> cpu_intensive
- large dataset processing -> memory_intensive
- real-time processing -> latency_sensitive
- low-latency request -> latency_sensitive
- ordinary task -> general

CPU rules:

If the user explicitly specifies CPU cores,
extract that value and set cpu_explicit to true.

If the user does not specify CPU cores:

- return a reasonable placeholder value
- set cpu_explicit to false

The workload profiler will later determine the
actual default CPU requirement.

Memory rules:

If the user explicitly specifies memory,
extract that value and set memory_explicit to true.

If the user does not specify memory:

- return a reasonable placeholder value
- set memory_explicit to false

The workload profiler will later determine the
actual default memory requirement.

GPU rules:

If the user explicitly requests a GPU,
set gpu_required to true and gpu_explicit to true.

If the workload clearly requires GPU processing,
such as image generation or deep learning:

- set gpu_required to true
- set gpu_explicit to false

If the user does not require GPU processing:

- set gpu_required to false
- set gpu_explicit to false

Deadline rules:

Only create deadline_seconds when the user explicitly
provides a deadline or time limit.

Examples:

- "within 10 seconds" -> 10
- "finish in 30 seconds" -> 30
- "within 2 minutes" -> 120

If no explicit deadline exists:

- deadline_seconds = null

Do NOT convert phrases such as:

- "as soon as possible"
- "quickly"
- "fast"
- "urgently"

into an invented numeric deadline.

Priority rules:

- critical -> 5
- highest priority -> 5
- urgent -> 5
- high priority -> 4
- high priority request -> 4
- medium priority -> 3
- normal priority -> 3
- low priority -> 1
- no priority specified -> 3

Important:

The user may express urgency without giving a
numeric deadline.

For example:

"Generate an image as soon as possible."

This should indicate a high-priority or urgent task,
but deadline_seconds must remain null.

User request:

{user_request}
"""

        response_format = {
            "type": "text",
            "mime_type": "application/json",
            "schema": {
                "type": "object",
                "properties": {
                    "workload_type": {
                        "type": "string",
                        "description": (
                            "Scheduling workload category."
                        )
                    },
                    "cpu_required": {
                        "type": "number",
                        "description": (
                            "CPU cores explicitly requested "
                            "by the user, or a placeholder "
                            "when not specified."
                        )
                    },
                    "cpu_explicit": {
                        "type": "boolean",
                        "description": (
                            "Whether the user explicitly "
                            "specified CPU requirements."
                        )
                    },
                    "memory_required_gb": {
                        "type": "number",
                        "description": (
                            "Memory in GB explicitly requested "
                            "by the user, or a placeholder "
                            "when not specified."
                        )
                    },
                    "memory_explicit": {
                        "type": "boolean",
                        "description": (
                            "Whether the user explicitly "
                            "specified memory requirements."
                        )
                    },
                    "gpu_required": {
                        "type": "boolean",
                        "description": (
                            "Whether GPU processing is required."
                        )
                    },
                    "gpu_explicit": {
                        "type": "boolean",
                        "description": (
                            "Whether the user explicitly "
                            "requested a GPU."
                        )
                    },
                    "deadline_seconds": {
                        "type": [
                            "number",
                            "null"
                        ],
                        "description": (
                            "Explicit task deadline in seconds, "
                            "or null when not specified."
                        )
                    },
                    "priority": {
                        "type": "integer",
                        "description": (
                            "Priority from 1 to 5."
                        )
                    }
                },
                "required": [
                    "workload_type",
                    "cpu_required",
                    "cpu_explicit",
                    "memory_required_gb",
                    "memory_explicit",
                    "gpu_required",
                    "gpu_explicit",
                    "deadline_seconds",
                    "priority"
                ]
            }
        }

        interaction = self.client.interactions.create(
            model=self.model,
            input=prompt,
            response_format=response_format
        )

        data = interaction.output_text

        try:
            parsed_data = json.loads(data)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Gemini structured output was not valid JSON: "
                + data
            ) from exc

        requirements = TaskRequirements(
            workload_type=parsed_data[
                "workload_type"
            ],
            cpu_required=parsed_data[
                "cpu_required"
            ],
            memory_required_gb=parsed_data[
                "memory_required_gb"
            ],
            gpu_required=parsed_data[
                "gpu_required"
            ],
            deadline_seconds=parsed_data[
                "deadline_seconds"
            ],
            priority=parsed_data[
                "priority"
            ]
        )

        requirements = WorkloadProfiler.apply_profile(
            requirements=requirements,
            cpu_explicit=parsed_data[
                "cpu_explicit"
            ],
            memory_explicit=parsed_data[
                "memory_explicit"
            ],
            gpu_explicit=parsed_data[
                "gpu_explicit"
            ]
        )

        return requirements