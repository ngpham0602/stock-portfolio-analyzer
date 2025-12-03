"""
Simple retry helper to practice loops, conditionals, and error handling.
"""
import time
from typing import Callable, Iterable, Type


def retry_call(func: Callable, retries: int = 3, backoff: float = 1.0, exceptions: Iterable[Type[BaseException]] = (Exception,)):
    """
    Call `func` with retries. This is deliberately written with explicit loops
    and conditionals so you can follow the flow.
    """
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            return func()
        except exceptions as err:  # type: ignore[arg-type]
            last_error = err
            is_last = attempt == retries - 1
            if is_last:
                break
            sleep_for = backoff * (attempt + 1)
            time.sleep(sleep_for)
    raise RuntimeError(f"Retry failed after {retries} attempts: {last_error}")
