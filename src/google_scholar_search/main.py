import bs4
import cli_arg_parser as ap
import importlib as il
import importlib.util as ilu
import logging as lg
import secrets
import sys
import umpyutl as umpy

from datetime import datetime as dt
from pathlib import Path
from types import ModuleType
from urllib.parse import urlencode

BASE_URL = "https://scholar.google.com"


def import_module(module_name: str, package_name: str | None = None) -> ModuleType:
    """TODO"""
    absolute_name = ilu.resolve_name(module_name, package_name)
    if ilu.find_spec(f".{absolute_name}", package_name):
        return il.import_module(f"{package_name}.{absolute_name}")
    else:
        raise ModuleNotFoundError("Plugin not located", name=absolute_name)

    # spec = ilu.spec_from_file_location(module_name, f"./{package_name}/{module_name}.py")
    # module = ilu.module_from_spec(spec)
    # spec.loader.exec_module(module)
    # return module


def retrieve_author_links(base_url: str, tag: bs4.Tag) -> list:
    """Return author citation links from passed-in bs4.Tag object.

    Parameters:
        html (bs4.Tag): Tag object

    Returns:
        list: sequence of author dictionaries
    """

    return [
        {"author_name": element.text, "url_fragment": f"{base_url}{element.get('href')}"}
        for element in tag.find_all("a", href=True)
    ]


def retrieve_citation(html) -> dict:
    """Return citation attributes from passed-in <html>.

    Parameters:
        html (BeautifulSoup.element.Tag): chunk of HTML

    Returns:
        dict: dictionary representation of a citation
    """

    return {
        "title": html.select_one(".gs_rt").text,
        "title_url": select_value_by_key(html.select_one(".gs_rt a"), "href"),
        "pub_info": html.select_one(".gs_a").text,
        "author_links": retrieve_author_links(BASE_URL, html.find("div", {"class": "gs_a"})),
        "snippet": html.select_one(".gs_rs").text,
        "cited_by": select_value_by_key(html.select_one("#gs_res_ccl_mid .gs_nph+ a"), "href"),
        "pdf_url": select_value_by_key(html.select_one(".gs_or_ggsm a:nth-child(1)"), "href"),
        # "related_articles": select_value_by_key(result.select_one("#gs_res_ccl_mid .gs_nph+ a+ a"), "href"),
    }


def select_value_by_key(selector, key):
    """Return a value from a selector object.

    Parameters:
        selector (obj): selector object
        key (str): key to retrieve

    Returns:
        str: value associated with key
    """

    try:
        return selector[key]
    except (KeyError, TypeError):
        return None


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

    plugin = import_module(plugin_name, "plugins")
    searcher = plugin.SearchPlugin()
    print(f"\nplugin max calls = {searcher.max_calls}")

    # TODO append 10 citations to existing JSON file (don't hold in memory all citations)

    citations = []
    for i in range(offset, limit):
        params: dict = {"start": i, "q": query, "hl": "en", "as_sdt": "0, 23"}
        gs_url: str = f"{BASE_URL}/scholar" + "?" + urlencode(params)
        json = {"apiKey": secrets.SCRAPERAPI_KEY, "url": gs_url}
        scraper_url = "https://async.scraperapi.com/jobs"
        data: dict = searcher.run_job(scraper_url, json)

        umpy.write.to_json(f"scarperapi_{i}.json", data)

        html: str = data["response"]["body"]
        filename: str = f"gs-html-{i}-{dt.now().strftime('%Y%m%dT%H%M')}.html"
        filepath: str = Path(__file__).parent.absolute().joinpath("output", filename)
        print(f"\nfilepath={filepath}")
        umpy.write.to_txt(filepath, [html])

        soup = bs4.BeautifulSoup(html, "lxml")
        for result in soup.select(".gs_r.gs_or.gs_scl"):
            citations.append(retrieve_citation(result))
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
