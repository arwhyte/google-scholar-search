from abc import ABC, abstractmethod


class Scraper(ABC):
    """TODO"""

    def __init__(self, base_url: str, html: str) -> None:
        self.base_url = base_url
        self.html = html

    @abstractmethod
    def scrape(self, html: str) -> list:
        """TODO"""
        pass
