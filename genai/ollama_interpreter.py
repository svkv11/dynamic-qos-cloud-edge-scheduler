import json
import requests

from genai.task_requirements import TaskRequirements
from genai.workload_profiler import WorkloadProfiler


class OllamaRequirementInterpreter:
    """
    Use a local Qwen model through Ollama to convert
    natural-language task requests into TaskRequirements.

    This interpreter is the local/offline alternative to
    GeminiRequirementInterpreter.
    """

    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL = "qwen3:4b-instruct"

    SYSTEM_PROMPT = """
You are the requirement interpretation component of a
Dynamic QoS Cloud-Edge Scheduler.

You are NOT an image generator.
You are NOT a general chatbot.

Your job is to understand the user's natural-language request
and extract only the scheduling requirements that can be
reasonably determined from what the user actually said.

Identify:

1. workload_type
2. gpu_required
3. priority
4. deadline_seconds
5. explicit_cpu_required
6. explicit_memory_required_gb

Workload types:

- general
- cpu_intensive
- memory_intensive
- gpu_intensive
- latency_sensitive

Priority:

1 = very low
2 = low
3 = normal
4 = high
5 = critical

Interpret natural language:

- "quickly", "as soon as possible", "urgent", "urgently"
  indicate higher priority.
- Do NOT convert words such as "quickly" or "fast" into
  an exact deadline unless the user explicitly gives
  a time limit.

IMPORTANT RESOURCE RULES:

- NEVER invent CPU requirements.
- NEVER invent memory requirements.
- NEVER invent a deadline.
- Only provide CPU if the user explicitly mentions a CPU
  requirement.
- Only provide memory if the user explicitly mentions a
  memory requirement.
- Only provide a deadline if the user explicitly gives
  a time limit.
- If the user does not provide one of these values, return null.
- GPU can be inferred from the nature of the workload.
- For gpu_intensive workloads, gpu_required MUST be true.
- For cpu_intensive, memory_intensive, latency_sensitive,
  and general workloads, gpu_required MUST be false unless
  the user explicitly requires a GPU.

OUTPUT FORMAT:

Return ONLY valid JSON using exactly these fields:

{
  "workload_type": "general",
  "gpu_required": false,
  "priority": 3,
  "deadline_seconds": null,
  "explicit_cpu_required": null,
  "explicit_memory_required_gb": null
}

IMPORTANT:

- gpu_required MUST always be either true or false.
- NEVER return null for gpu_required.
- Do not omit any field.
- Do not include explanations.
- Do not use Markdown.
"""

    def __init__(self):
        self.model = self.MODEL

    def interpret(self, user_request):
        prompt = f"""
{self.SYSTEM_PROMPT}

User request:
{user_request}
"""

        response = requests.post(
            self.OLLAMA_URL,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Ollama request failed. "
                f"Status code: {response.status_code}. "
                f"Response: {response.text}"
            )

        result = response.json()

        llm_output = result.get(
            "response",
            ""
        ).strip()

        if not llm_output:
            raise ValueError(
                "Qwen returned an empty response."
            )

        if llm_output.startswith("```"):
            lines = llm_output.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            llm_output = "\n".join(lines).strip()

        try:
            data = json.loads(llm_output)

        except json.JSONDecodeError as error:
            raise ValueError(
                "Qwen returned invalid JSON.\n"
                f"Raw response:\n{llm_output}"
            ) from error

        required_fields = [
            "workload_type",
            "gpu_required",
            "priority",
            "deadline_seconds",
            "explicit_cpu_required",
            "explicit_memory_required_gb"
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(
                    "Qwen response is missing required "
                    f"field: {field}"
                )

        gpu_required = data["gpu_required"]

        if isinstance(gpu_required, str):
            gpu_value = gpu_required.strip().lower()

            if gpu_value == "true":
                gpu_required = True

            elif gpu_value == "false":
                gpu_required = False

            elif gpu_value in {"null", "none", ""}:
                gpu_required = None

            else:
                raise ValueError(
                    "Qwen returned an invalid gpu_required value: "
                    f"{gpu_required}"
                )

        elif gpu_required is not None and not isinstance(
            gpu_required,
            bool
        ):
            raise ValueError(
                "Qwen returned an invalid gpu_required value: "
                f"{gpu_required}"
            )

        if gpu_required is None:
            if data["workload_type"] == "gpu_intensive":
                gpu_required = True
            else:
                gpu_required = False

        requirements = TaskRequirements(
            workload_type=data["workload_type"],
            cpu_required=(
                data["explicit_cpu_required"]
                if data["explicit_cpu_required"] is not None
                else 1
            ),
            memory_required_gb=(
                data["explicit_memory_required_gb"]
                if data["explicit_memory_required_gb"] is not None
                else 1
            ),
            gpu_required=gpu_required,
            deadline_seconds=data["deadline_seconds"],
            priority=data["priority"]
        )

        requirements = WorkloadProfiler.apply_profile(
            requirements=requirements,
            cpu_explicit=(
                data["explicit_cpu_required"] is not None
            ),
            memory_explicit=(
                data["explicit_memory_required_gb"] is not None
            ),
            gpu_explicit=True
        )

        return requirements