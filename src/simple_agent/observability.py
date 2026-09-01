import json
import logging
import time
from contextlib import contextmanager
from typing import Iterator

LOGGER = logging.getLogger("simple_agent")


def configure_logging() -> None:
    if LOGGER.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.INFO)


def log_event(event: str, **fields: object) -> None:
    configure_logging()
    LOGGER.info(json.dumps({"event": event, **fields}, default=str))


@contextmanager
def latency_timer() -> Iterator[dict[str, float]]:
    state: dict[str, float] = {}
    started = time.perf_counter()
    try:
        yield state
    finally:
        state["latency_ms"] = (time.perf_counter() - started) * 1000
