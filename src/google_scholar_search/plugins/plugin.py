from abc import ABC, abstractmethod

class Plugin(ABC):
    """TODO"""

    @abstractmethod
    def scrape(self, query: str) -> str:
        """TODO"""
        pass
