from abc import ABC, abstractmethod


class Plugin(ABC):
    """TODO"""

    def __init__(self, call_interval: int, max_calls: int, timeout: int) -> None:
        self.call_interval = call_interval
        self.max_calls = max_calls
        self.timeout = timeout
