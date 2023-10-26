import bs4
import cli_arg_parser as ap
import logging
import requests
import secrets
import sys
import time
import umpyutl as umpy
import user_agents as ua

from datetime import datetime as dt
from pathlib import Path
from urllib.parse import urlencode

BASE_URL = "https://scholar.google.com"


def filter_data(data: dict, keys: tuple) -> dict:
    """Filters out article key-value pairs in favor of the select keys contained
    in the passed in < keys > tuple.

    Parameters:
        data (list): list of nested article dictionaries
        keys (tuple): key-value pairs to retain

    Returns:
        dict: new dictionary containing a subset of the original key-value pairs
    """

    return {key: val for key, val in data.items() if key in keys}


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


# def run_async_job(
#     url, json, timeout, call_interval=5, max_calls=1000, max_retries=5, retry_interval=60
# ):
#     """TODO"""

#     response: requests.Response = requests.post(url=url, json=json, timeout=timeout)
#     response.raise_for_status()  # raises HTTPError if one occurred
#     response: dict = response.json()
#     status: str = response["status"]
#     status_url: str = response["statusURL"]

#     calls: int = 0
#     while not status == "finished" and calls < max_calls:
#         time.sleep(call_interval)
#         response: requests.Response = requests.get(status_url, timeout=timeout)
#         response.raise_for_status()  # raises HTTPError if one occurred
#         response: dict = response.json()
#         status = response["status"].lower()
#         calls += 1
#     return response


def run_async_job(url, json, timeout=10, call_interval=5, max_calls=1000) -> dict:
    """TODO"""

    response: requests.Response = requests.post(url=url, json=json, timeout=timeout)
    response.raise_for_status()  # raises HTTPError if one occurred
    data: dict = response.json()
    status: str = data["status"]
    status_url: str = data["statusUrl"]
    print(f"\nrun_async_job data={data}")

    calls: int = 0
    while not status == "finished" and calls < max_calls:
        time.sleep(call_interval)
        response: requests.Response = requests.get(status_url, timeout=timeout)
        response.raise_for_status()  # raises HTTPError if one occurred
        data: dict = response.json()
        status = data["status"].lower()
        calls += 1
    return data


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


def main(args: list) -> None:
    """Entry point to script. Orchestrates workflow.

    Parameters:
        args (list): CLI arguments

    Returns:
        None
    """

    # Configure logger: set format and default level
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    logger = logging.getLogger()
    logger.addHandler(logging.FileHandler("./log/google_scholar-articles.log"))
    # logger.addHandler(logging.StreamHandler(sys.stdout))

    # Parse CLI args
    parser = ap.create_parser("google_scholar_search")
    cli_args = parser.parse_args(args)
    offset: int = cli_args.offset
    limit: int = cli_args.limit
    query: str = cli_args.query

    # load YAML config retrieve querystring params
    # config = umpy.read.from_yaml("./config.yml")
    # params = config["params"][params_name]  # Get desired querystring
    # params["api-key"] = secrets.API_KEY  # Add secret API key

    # Log requests
    logger.info(f"START RUN: {dt.now().isoformat()}")
    logger.info(f"Query: {query}")
    logger.info(f"Offset: {offset}")
    logger.info(f"Limit: {limit}")

    # TODO append 10 citations to existing JSON file (don't hold in memory all citations)

    citations = []
    for i in range(offset, limit):
        params: dict = {"start": i, "q": query, "hl": "en", "as_sdt": "0, 23"}
        gs_url: str = f"{BASE_URL}/scholar" + "?" + urlencode(params)
        json = {
            "apiKey": secrets.SCRAPERAPI_KEY,
            'url': gs_url
        }
        scraper_url = "https://async.scraperapi.com/jobs"

        data: dict = run_async_job(scraper_url, json)

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
    main(sys.argv[1:])  # ignore the first element (program name)
