import time
from typing import Callable, TypeVar

T = TypeVar("T")

def retry_until(
    fn: Callable[[], T],
    *,
    timeout_s: int = 120,
    interval_s: float = 2.0,
    on_retry: Callable[[Exception], None] | None = None,
) -> T:
    end = time.time() + timeout_s
    last_exc: Exception | None = None
    while time.time() < end:
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if on_retry:
                on_retry(e)
            time.sleep(interval_s)
    raise TimeoutError(f"Timed out after {timeout_s}s. Last error: {last_exc}")
