"""Page object pattern and selenium decorators"""
import logging
from functools import wraps
from time import sleep
from typing import Any
from typing import Callable
from typing import Optional

from selenium.common import WebDriverException


def retry_on_selenium_error(times_to_try: int = 3, seconds_to_wait: int = 1):
    """Decorator for selenium to retry a specific number of times on failure

    :param times_to_try: times to call a function
    :param seconds_to_wait: time in seconds to wait between retries
    """

    def decorator(selenium_method: Callable):
        @wraps(selenium_method)
        def wrapper(*args: Any, **kwargs: Any):
            last_error: Optional[WebDriverException] = None
            for try_number in range(times_to_try):
                try:
                    return selenium_method(*args, **kwargs)
                except WebDriverException as error:
                    last_error = error
                    logging.warning(
                        "Error during `%s` selenium function. Attempts to retry %s/%s. Retry in %s seconds",
                        selenium_method.__name__,
                        try_number + 1,
                        times_to_try,
                        seconds_to_wait,
                    )
                sleep(seconds_to_wait)
            logging.error("Max tries reached for selenium method `%s`. Raising error", selenium_method.__name__)
            raise last_error

        return wrapper

    return decorator
