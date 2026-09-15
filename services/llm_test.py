import requests

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

Examples:

User:
"Create an AI image quickly."

Return:
{
  "workload_type": "gpu_intensive",
  "gpu_required": true,
  "priority": 4,
  "deadline_seconds": null,
  "explicit_cpu_required": null,
  "explicit_memory_required_gb": null
}

User:
"Run my model using 8 CPU cores and 16 GB RAM within 20 seconds."

Return:
{
  "workload_type": "cpu_intensive",
  "gpu_required": false,
  "priority": 3,
  "deadline_seconds": 20,
  "explicit_cpu_required": 8,
  "explicit_memory_required_gb": 16
}

Return ONLY valid JSON.
Do not include explanations.
Do not use Markdown.
"""


user_request = "Run my model using 8 CPU cores and 16 GB RAM within 20 seconds."


prompt = f"""
{SYSTEM_PROMPT}

User request:
{user_request}
"""


response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
)


if response.status_code == 200:
    result = response.json()

    print("=" * 60)
    print("LLM REQUIREMENT INTERPRETATION TEST")
    print("=" * 60)

    print("\nUser Request:")
    print(user_request)

    print("\nQwen Response:")
    print(result["response"])

else:
    print("Error communicating with Ollama")
    print("Status Code:", response.status_code)
    print(response.text)