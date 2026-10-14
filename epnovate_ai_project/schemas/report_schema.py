from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class NewsArticle(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    published_at: str | None = None
    source: str = "Unknown"


class ReportData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic: str = Field(min_length=1)
    generated_at: str
    articles: list[NewsArticle]
    market_metrics: dict
    compliance: dict
    summary: str = Field(min_length=1)
    synthesis_mode: str = "template"
