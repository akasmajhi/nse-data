from time import perf_counter
from typing import Any, Callable
from loguru import logger


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwrgs: Any) -> Any:
        start_time = perf_counter()
        value = func(*args, **kwrgs)
        end_time = perf_counter()
        logger.info(
            f"Finished [{func.__name__}] in [{(end_time-start_time):.2f}] seconds."
        )
        return value

    return wrapper
