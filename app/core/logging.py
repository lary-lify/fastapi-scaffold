import json
import logging
import sys

from app.core.config import settings


class _JsonFormatter(logging.Formatter):
    """Emit one-line JSON per record for production log aggregators."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging() -> None:
    """Configure the root logger: JSON in production, plain text in DEBUG."""
    handler = logging.StreamHandler(sys.stdout)
    if settings.DEBUG:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )
        level = logging.DEBUG
    else:
        handler.setFormatter(_JsonFormatter())
        level = logging.INFO

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
