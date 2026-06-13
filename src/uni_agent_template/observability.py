from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from typing import Iterator

logger = logging.getLogger("uni_agent_template")


@contextmanager
def timed_stage(name: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        logger.debug("stage=%s elapsed_ms=%.2f", name, (time.perf_counter() - start) * 1000)
