import functools
import time

import pyinstrument
from src.utils import LOGGER


def time_profiling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        LOGGER.info(
            f"Function {func.__name__} executed in {time.time() - start_time:.4f} seconds."
        )
        return result

    return wrapper


def async_time_profiling(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        LOGGER.info(
            f"Function {func.__name__} executed in {time.time() - start_time:.4f} seconds."
        )
        return result

    return wrapper


def async_py_profiling(func):
    async def wrapper(*args, **kwargs):
        profiler = pyinstrument.Profiler(async_mode="enabled")
        profiler.start()
        result = await func(*args, **kwargs)
        profiler.stop()
        with open(f"./logs/time_execute_{func.__name__}.html", "w") as f:
            f.write(profiler.output_html())
        return result

    return wrapper


def py_profiling(func):
    def wrapper(*args, **kwargs):
        profiler = pyinstrument.Profiler()
        profiler.start()
        result = func(*args, **kwargs)
        profiler.stop()
        with open(f"./logs/time_execute_{func.__name__}.html", "w") as f:
            f.write(profiler.output_html())
        return result

    return wrapper
