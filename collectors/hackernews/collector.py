"""
Hacker News collector (safe fallback version).

Avoids network dependency for GitHub Actions.
"""

def collect_hackernews():
    """
    Collect Hacker News stories.
    Fallback implementation for CI / demo.
    """
    return {
        "source": "hackernews",
        "results": [
            {
                "text": "Discussion on Hacker News about monitoring AI safety risks",
                "meta": {
                    "type": "story",
                    "score": 42
                }
            }
        ]
    }
