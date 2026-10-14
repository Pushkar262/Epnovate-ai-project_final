from config import settings


def get_market_benchmarks(topic: str) -> dict:
    """
    Retrieve internal market metrics.

    MOCK mode is for local development only. Set MCP_MODE=real after
    implementing the client call using the MCP server details supplied
    by the assessment environment.
    """
    if settings.mcp_mode == "mock":
        return {
            "mode": "mock",
            "topic": topic,
            "enterprise_adoption_rate": None,
            "sentiment": "not_available",
            "cost_index": None,
            "note": (
                "Mock response: replace with real MCP data before "
                "presenting this as company information."
            ),
        }

    raise NotImplementedError(
        "Real MCP integration requires the provided server transport, "
        "authentication, and get_market_benchmarks tool schema."
    )
