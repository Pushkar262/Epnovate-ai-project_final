from schemas.report_schema import NewsArticle, ReportData


def test_news_article_schema():
    article = NewsArticle(
        title="Example", url="https://example.com", source="Example"
    )
    assert article.title == "Example"


def test_report_data_schema():
    report = ReportData(
        topic="AI",
        generated_at="2026-10-14T00:00:00+00:00",
        articles=[],
        market_metrics={"mode": "mock"},
        compliance={"status": "not_assessed"},
        summary="Mock report",
        synthesis_mode="template",
    )
    assert report.topic == "AI"
