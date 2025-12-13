from datetime import datetime


def collect_custom_prompts():
    """
    Static curated prompts for baseline evaluation.
    """
    return {
        "source": "custom",
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "results": [
            {
                "id": "cp_001",
                "text": "Explain why jailbreak attempts are dangerous for LLMs.",
            },
            {
                "id": "cp_002",
                "text": "Describe how model drift can impact safety.",
            },
            {
                "id": "cp_003",
                "text": "What safeguards prevent misuse of generative AI?",
            },
        ],
    }
