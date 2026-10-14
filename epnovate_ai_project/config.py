import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "AI Market Intelligence")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "15"))
    news_rss_url: str = os.getenv(
        "NEWS_RSS_URL", "https://news.google.com/rss/search"
    )
    mcp_mode: str = os.getenv("MCP_MODE", "mock").lower()
    mcp_server_command: str = os.getenv("MCP_SERVER_COMMAND", "")
    mcp_server_args: str = os.getenv("MCP_SERVER_ARGS", "")
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "")
    mcp_transport: str = os.getenv("MCP_TRANSPORT", "stdio").lower()
    llm_provider: str = os.getenv("LLM_PROVIDER", "").lower()
    llm_model: str = os.getenv("LLM_MODEL", "")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    pdf_output_path: str = os.getenv(
        "PDF_OUTPUT_PATH", "reports/market_intelligence_report.pdf"
    )
    max_articles: int = int(os.getenv("MAX_ARTICLES", "10"))


settings = Settings()
