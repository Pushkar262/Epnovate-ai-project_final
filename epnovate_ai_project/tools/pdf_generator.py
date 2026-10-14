import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
)

from config import settings
from schemas.report_schema import ReportData


def _json_text(value: dict) -> str:
    return escape(json.dumps(value, indent=2, ensure_ascii=False))


def render_pdf_report(data: ReportData, output_path: str | None = None) -> str:
    path = Path(output_path or settings.pdf_output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="SmallBody", parent=styles["BodyText"], fontSize=8,
        leading=11, spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name="JsonBlock", parent=styles["Code"], fontSize=7,
        leading=9, wordWrap="CJK", spaceAfter=8
    ))

    doc = SimpleDocTemplate(
        str(path), pagesize=A4,
        rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title=f"AI Market Intelligence: {data.topic}",
        author="AI Market Intelligence System",
    )

    story = [
        Paragraph("AI Market Intelligence Report", styles["Title"]),
        Spacer(1, 6 * mm),
        Paragraph(f"<b>Topic:</b> {escape(data.topic)}", styles["Heading2"]),
        Paragraph(f"<b>Generated (UTC):</b> {escape(data.generated_at)}",
                  styles["SmallBody"]),
        Paragraph(f"<b>Synthesis mode:</b> {escape(data.synthesis_mode)}",
                  styles["SmallBody"]),
        Spacer(1, 4 * mm),
        Paragraph("Executive Summary", styles["Heading2"]),
        Paragraph(escape(data.summary), styles["BodyText"]),
        Spacer(1, 4 * mm),
        Paragraph("Market Metrics", styles["Heading2"]),
        Paragraph(f"<pre>{_json_text(data.market_metrics)}</pre>",
                  styles["JsonBlock"]),
        Paragraph("Compliance Findings", styles["Heading2"]),
        Paragraph(f"<pre>{_json_text(data.compliance)}</pre>",
                  styles["JsonBlock"]),
        Paragraph(f"Recent News ({len(data.articles)} articles)",
                  styles["Heading2"]),
    ]

    for index, article in enumerate(data.articles, start=1):
        block = [
            Paragraph(f"{index}. {escape(article.title)}", styles["Heading3"]),
            Paragraph(f"Source: {escape(article.source)}", styles["SmallBody"]),
            Paragraph(f"URL: {escape(article.url)}", styles["SmallBody"]),
            Paragraph(
                f"Published: {escape(article.published_at or 'Unknown')}",
                styles["SmallBody"],
            ),
            Spacer(1, 2 * mm),
        ]
        story.append(KeepTogether(block))

    def add_page_number(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(
            A4[0] - 18 * mm, 10 * mm, f"Page {document.page}"
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return str(path)
