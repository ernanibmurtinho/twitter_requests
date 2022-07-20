import time
from functools import wraps


class TimerDecorator:
    """
    Time counter decorator class.
    """

    def __init__(self, page_limit=1, count_tweet=100):
        """
        Instantiate TimerDecorator with page limit and number of requests default.

        :param int page_limit: Maximum number of pages of the requests.
        :param int count_tweet: Maximum number of tweets per request.
        """
        self.page_limit = page_limit
        self.count_tweet = count_tweet

    def timer(self, func):
        """Print the runtime of the decorated function"""

        @wraps(func)
        def wrapper_timer(*args, **kwargs):
            count_tweet = self.count_tweet
            start_time = time.perf_counter()  # 1
            print(f"Started {func.__name__!r} calling {count_tweet} requests ")
            value = func(*args, **kwargs)
            end_time = time.perf_counter()  # 2
            run_time = end_time - start_time  # 3
            print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
            print(f"The average time for requests {func.__name__!r} are {run_time / count_tweet:.4f} secs")
            return value

        return wrapper_timer
