import asyncio
import requests
import time

from plugins.plugin import Plugin


class SearchPlugin(Plugin):
    """TODO"""

    def __init__(self, call_interval: int = 5, max_calls: int = 100, timeout: int = 10) -> None:
        super().__init__(call_interval, max_calls, timeout)

    def __str__(self) -> str:
        return "ScraperAPI plugin"

    def scrape(self, query: str) -> str:
        """TODO"""
        pass

    def run_job(self, url, json) -> dict:
        """TODO"""

        response: requests.Response = requests.post(url=url, json=json, timeout=self.timeout)
        response.raise_for_status()  # raises HTTPError if one occurred

        data: dict = response.json()
        status: str = data["status"]
        status_url: str = data["statusUrl"]
        # print(f"\nrun_job data={data}")

        calls: int = 0
        while not status == "finished" and calls < self.max_calls:
            # await asyncio.sleep(self.call_interval)
            time.sleep(self.call_interval)

            response: requests.Response = requests.get(status_url, timeout=self.timeout)
            response.raise_for_status()  # raises HTTPError if one occurred

            data: dict = response.json()
            status = data["status"].lower()
            calls += 1
        return data
