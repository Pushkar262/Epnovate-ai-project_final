# AI Market Intelligence Report Generator

A modular Python scaffold for the AI/ML Engineer assessment.

## Architecture
1. `scrape_news_articles`: public Google News RSS retrieval.
2. `get_market_benchmarks`: internal market metrics via MCP (integration pending).
3. `check_compliance_risks`: compliance findings via MCP (integration pending).
4. `synthesize_insights`: validates and combines inputs; currently uses an honest template fallback unless a provider adapter is implemented.
5. `render_pdf_report`: creates a PDF using ReportLab.
6. `orchestrator.py`: coordinates the workflow.

## Setup
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

## Run locally
The default `MCP_MODE=mock` is for testing only and clearly labels mock/unassessed results.
```bash
python main.py --topic "enterprise AI adoption"
```
The PDF is written to `reports/market_intelligence_report.pdf`.

## Tests
```bash
pytest -q
```

## Before production / assessment submission
- Connect to the actual MCP server and use its advertised tool names and schemas.
- Implement the LLM adapter for the provider specified by the assessment.
- Add authentication, least-privilege access, bounded retries, and source/evidence checks.
- Never present mock metrics or mock compliance results as actual company findings.
- Do not commit `.env` or credentials.
