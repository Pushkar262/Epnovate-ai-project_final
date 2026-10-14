from config import settings
from schemas.report_schema import NewsArticle


def check_compliance_risks(
    topic: str, articles: list[NewsArticle]
) -> dict:
    """
    Check compliance through MCP. The mock response is not legal advice
    and must not be represented as a real compliance assessment.
    """
    if settings.mcp_mode == "mock":
        return {
            "mode": "mock",
            "topic": topic,
            "status": "not_assessed",
            "risks": [],
            "note": (
                "Mock response: no actual regulatory or compliance "
                "assessment has been performed."
            ),
            "articles_considered": len(articles),
        }

    raise NotImplementedError(
        "Real MCP integration requires the provided server transport, "
        "authentication, and check_compliance_risks tool schema."
    )
