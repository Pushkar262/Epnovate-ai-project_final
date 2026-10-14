import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests

from config import settings
from schemas.report_schema import NewsArticle

logger = logging.getLogger(__name__)


def scrape_news_articles(topic: str) -> list[NewsArticle]:
    """Fetch up to MAX_ARTICLES news items from Google News RSS."""
    if not topic.strip():
        raise ValueError("Topic cannot be empty")

    response = requests.get(
        settings.news_rss_url,
        params={"q": topic, "hl": "en-US", "gl": "US", "ceid": "US:en"},
        timeout=settings.request_timeout,
        headers={"User-Agent": "AI-Market-Intelligence/1.0"},
    )
    response.raise_for_status()

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as exc:
        raise ValueError("News provider returned invalid RSS/XML") from exc

    articles: list[NewsArticle] = []
    for item in root.findall(".//item")[: settings.max_articles]:
        title = (item.findtext("title") or "").strip()
        url = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        source = item.findtext("source") or "Google News RSS"

        published_at = None
        if pub_date:
            try:
                parsed = parsedate_to_datetime(pub_date)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                published_at = parsed.isoformat()
            except (TypeError, ValueError, OverflowError):
                logger.warning("Could not parse publication date: %s", pub_date)

        if title and url:
            articles.append(
                NewsArticle(
                    title=title,
                    url=url,
                    published_at=published_at,
                    source=source,
                )
            )

    logger.info("Retrieved %d articles for topic %r", len(articles), topic)
    return articles
