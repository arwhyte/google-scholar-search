from plugins.plugin import Plugin


class SearchPlugin(Plugin):
    """TODO"""

    def __init__(self, call_interval: int = 5, max_calls: int = 100, timeout: int = 10) -> None:
        super().__init__(call_interval, max_calls, timeout)

    def __str__(self) -> str:
        return "Scrapingbee plugin"
