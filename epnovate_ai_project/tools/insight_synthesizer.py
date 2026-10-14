import logging
from datetime import datetime, timezone

from config import settings
from schemas.report_schema import NewsArticle, ReportData

logger = logging.getLogger(__name__)


def _deterministic_summary(topic: str, articles: list[NewsArticle],
                          metrics: dict, compliance: dict) -> str:
    """Honest fallback: no LLM call is made in this mode."""
    return (
        f"This report covers {topic!r} and contains {len(articles)} "
        "retrieved news articles. Review the market metrics and "
        "compliance status below. Any mock or unavailable values must "
        "not be treated as verified company findings."
    )


def _llm_summary(topic: str, articles: list[NewsArticle],
                 metrics: dict, compliance: dict) -> str:
    """
    Provider-specific LLM implementation intentionally left configurable.
    Implement this using the provider/model required by the assessment.
    Pass only authorized, minimized internal data to the model.
    """
    if not settings.llm_provider or not settings.llm_model or not settings.llm_api_key:
        logger.info("LLM credentials/config not set; using deterministic summary")
        return _deterministic_summary(topic, articles, metrics, compliance)

    raise NotImplementedError(
        "LLM provider adapter is not configured. Implement the SDK call "
        "for the provider specified by the assessment."
    )


def synthesize_insights(topic: str, articles: list[NewsArticle],
                        metrics: dict, compliance: dict) -> ReportData:
    if not isinstance(metrics, dict):
        raise ValueError("Market metrics must be a dictionary")
    if not isinstance(compliance, dict):
        raise ValueError("Compliance findings must be a dictionary")

    summary = _llm_summary(topic, articles, metrics, compliance)
    return ReportData(
        topic=topic,
        generated_at=datetime.now(timezone.utc).isoformat(),
        articles=articles,
        market_metrics=metrics,
        compliance=compliance,
        summary=summary,
        synthesis_mode=(
            "llm" if settings.llm_provider and settings.llm_model
            and settings.llm_api_key else "template"
        ),
    )
