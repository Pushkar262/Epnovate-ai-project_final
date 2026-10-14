from orchestrator import run_pipeline


def test_pipeline_with_mock_mode(monkeypatch, tmp_path):
    import orchestrator

    monkeypatch.setattr(
        orchestrator, "scrape_news_articles", lambda topic: []
    )
    monkeypatch.setattr(
        orchestrator, "get_market_benchmarks",
        lambda topic: {"mode": "mock", "topic": topic}
    )
    monkeypatch.setattr(
        orchestrator, "check_compliance_risks",
        lambda topic, articles: {"status": "not_assessed"}
    )

    output = tmp_path / "report.pdf"
    monkeypatch.setattr(
        orchestrator, "render_pdf_report", lambda report: str(output)
    )
    assert run_pipeline("AI") == str(output)
