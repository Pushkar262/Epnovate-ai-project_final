import logging
from pathlib import Path

from tools.news_scraper import scrape_news_articles
from tools.market_benchmarks import get_market_benchmarks
from tools.compliance_checker import check_compliance_risks
from tools.insight_synthesizer import synthesize_insights
from tools.pdf_generator import render_pdf_report

logger = logging.getLogger(__name__)


def run_pipeline(topic: str) -> str:
    """Run the end-to-end workflow in dependency order."""
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic cannot be empty")

    logger.info("Step 1/5: Fetching public news")
    articles = scrape_news_articles(topic)

    logger.info("Step 2/5: Retrieving market benchmarks")
    metrics = get_market_benchmarks(topic)

    logger.info("Step 3/5: Checking compliance risks")
    compliance = check_compliance_risks(topic, articles)

    logger.info("Step 4/5: Synthesizing and validating insights")
    report = synthesize_insights(topic, articles, metrics, compliance)

    logger.info("Step 5/5: Rendering PDF")
    output_path = render_pdf_report(report)
    logger.info("Report saved to %s", output_path)
    return output_path
