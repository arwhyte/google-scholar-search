import bs4
import cli_arg_parser as ap
import importlib as il
import importlib.util as ilu
import logging as lg
import soup_scraper as soup
import secrets
import sys
import umpyutl as umpy

from datetime import datetime as dt
from pathlib import Path
from types import ModuleType
from urllib.parse import urlencode

BASE_URL = "https://scholar.google.com"


def import_plugin(module_name: str, package_name: str | None = None) -> ModuleType:
    """TODO"""
    absolute_name = ilu.resolve_name(f".{module_name}", package_name)
    if ilu.find_spec(absolute_name):
        return il.import_module(absolute_name)
    else:
        raise ModuleNotFoundError("Plugin not located", name=absolute_name)

    # spec = ilu.spec_from_file_location(module_name, f"./{package_name}/{module_name}.py")
    # module = ilu.module_from_spec(spec)
    # spec.loader.exec_module(module)
    # return module


def main(args):
    """TODO"""

    # Configure logger: set format and default level
    lg.basicConfig(format="%(levelname)s: %(message)s", level=lg.DEBUG)
    logger = lg.getLogger()
    logger.addHandler(lg.FileHandler("./log/google_scholar-articles.log"))
    # logger.addHandler(logging.StreamHandler(sys.stdout))

    logger.info(f"START RUN: {dt.now().isoformat()}")

    parser = ap.create_parser("Web Scraper")
    cli_args = parser.parse_args(args)
    plugin_name: str = cli_args.plugin
    query: str = cli_args.query
    offset: int = cli_args.offset
    limit: int = cli_args.limit

    logger.info(f"Plugin: {plugin_name}")
    logger.info(f"Query: {query}")
    logger.info(f"Offset: {offset}")
    logger.info(f"Limit: {limit}")

    plugin = import_plugin(plugin_name, "plugins")
    searcher = plugin.SearchPlugin()
    print(f"\nplugin max calls = {searcher.max_calls}")

    # TODO append 10 citations to existing JSON file (don't hold in memory all citations)

    citations = []
    for i in range(offset, limit):
        params: dict = {"start": i, "q": query, "hl": "en", "as_sdt": "0, 23"}
        gs_url: str = f"{BASE_URL}/scholar" + "?" + urlencode(params)
        json = {"url": gs_url}

        data: dict = searcher.run_async_job(searcher.async_endpoint, json)

        html: str = data["response"]["body"]
        filename: str = f"gs-html-{i}-{dt.now().strftime('%Y%m%dT%H%M')}.html"
        filepath: str = Path(__file__).parent.absolute().joinpath("output", filename)
        print(f"\nfilepath={filepath}")
        umpy.write.to_txt(filepath, [html])

        citations.extend(soup.SoupScraper(BASE_URL, html).scrape())
        logger.info(f"Citation successfully retrieved and appended to list.")

    # Write to file
    filepath = f"./output/google_scholar-ummz-bird-{dt.now().strftime('%Y%m%dT%H%M')}.json"
    umpy.write.to_json(filepath, citations)
    logger.info(f"File written to {filepath}")

    # logger.info(f"Total articles retrieved = {len(articles)}")

    # End run
    logger.info(f"END RUN: {dt.now().isoformat()}")


if __name__ == "__main__":
    main(sys.argv[1:])
