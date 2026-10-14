import argparse
import logging

from dotenv import load_dotenv

# Load .env before importing modules that read settings.
load_dotenv()

from config import settings
from orchestrator import run_pipeline
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI Market Intelligence PDF report generator"
    )
    parser.add_argument("--topic", required=False, help="Topic to research")
    args = parser.parse_args()

    topic = (args.topic or input("Enter a topic: ")).strip()
    if not topic:
        parser.error("Topic cannot be empty")

    try:
        output = run_pipeline(topic)
        print(f"Report generated: {output}")
    except Exception:
        logger.exception("Pipeline failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
