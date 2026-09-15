import json
import requests


class LLMRequirementInterpreter:
    """
    Uses a local Qwen model through Ollama to convert
    natural-language workload requests into structured
    scheduling requirements.
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

- normal
- cpu_intensive
- memory_intensive
- gpu_intensive

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
  an exact deadline unless the user explicitly gives a
  time limit.

IMPORTANT RESOURCE RULES:

- NEVER invent CPU requirements.
- NEVER invent memory requirements.
- NEVER invent a deadline.
- Only provide CPU if the user explicitly mentions a CPU
  requirement.
- Only provide memory if the user explicitly mentions a
  memory requirement.
- Only provide a deadline if the user explicitly gives a
  time limit.
- If the user does not provide one of these values, return null.
- GPU can be inferred from the nature of the workload.
  For example, AI image generation or deep learning normally
  requires GPU acceleration.

Return ONLY valid JSON.
Do not include explanations.
Do not use Markdown.
"""

    @classmethod
    def interpret(cls, user_request):
        """
        Send a natural-language request to Qwen through Ollama
        and return structured scheduling requirements.
        """

        prompt = f"""
{cls.SYSTEM_PROMPT}

User request:
{user_request}
"""

        response = requests.post(
            cls.OLLAMA_URL,
            json={
                "model": cls.MODEL,
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

        llm_output = result.get("response", "").strip()

        if not llm_output:
            raise ValueError(
                "Qwen returned an empty response."
            )

        # Remove Markdown code fences if the model
        # unexpectedly adds them.
        if llm_output.startswith("```"):
            lines = llm_output.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            llm_output = "\n".join(lines).strip()

        try:
            requirements = json.loads(llm_output)

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
            if field not in requirements:
                raise ValueError(
                    f"Qwen response is missing required field: {field}"
                )

        return requirements