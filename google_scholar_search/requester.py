import argparse
import json
import logging
import lxml
import requests
import secrets
import sys
import time
import umpyutl as umpy
import user_agents as ua

from bs4 import BeautifulSoup
from datetime import datetime as dt

BASE_URL = "https://scholar.google.com/scholar"
KEYS = ()


def create_parser():
    """Return a custom argument parser.

    Parameters:
       None

    Parser arguments:
        short_flag (str): short version of command option
        long_flag (str): long version of command option
        type (str): argument type (e.g., str, int, bool)
        required (bool): specifies whether or not command option is required
        default (obj): default value, typically str or int
        help (str): short description of command option

    Returns:
        parser (ArgumentParser): parser object
    """

    parser = argparse.ArgumentParser("Google Scholar requester.")
    # parser.add_argument(
    #     "-p",
    #     "--params_name",
    #     type=str,
    #     required=True,
    #     help=("Name of params dictionary stored in a config file."),
    # )
    parser.add_argument(
        "-r",
        "--requests_count",
        type=int,
        required=False,
        default=1,
        help=(
            "Number of API requests (paged response = 10 records). Default requests_count = 1."
        ),
    )
    return parser


def filter_data(data: list, keys: tuple) -> dict:
    """Filters out article key-value pairs in favor of the select keys contained
    in the passed in < keys > tuple.

    Parameters:
        data (list): list of nested article dictionaries
        keys (tuple): key-value pairs to retain

    Returns:
        dict: new dictionary containing a subset of the original key-value pairs
    """

    return {key: val for key, val in data.items() if key in keys}


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
    """Entry point to script."""

    # Configure logger: set format and default level
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    logger = logging.getLogger()
    logger.addHandler(logging.FileHandler("./log/google_scholar-articles.log"))
    # logger.addHandler(logging.StreamHandler(sys.stdout))

    # Parse CLI args
    parser = create_parser().parse_args(args)
    # params_name = parser.params_name
    requests_count = parser.requests_count

    # load YAML config retrieve querystring params
    # config = umpy.read.from_yaml("./config.yml")
    # params = config["params"][params_name]  # Get desired querystring
    # params["api-key"] = secrets.API_KEY  # Add secret API key

    # Log requests
    logger.info(f"START RUN: {dt.now().isoformat()}")
    # logger.info(f"Query: {params['q']}")
    # if params.get("fq"):
    #     logger.info(f"Filter: {params['fq']}")
    logger.info(f"Requests count = {requests_count}")

    citations = (
        []
    )  # TODO append 10 citations to existing JSON file (don't hold in memory all citations)
    for i in range(requests_count):
        # params["page"] = i  # reset

        # https://scholar.google.com/scholar?start=10&q=UMMZ+bird&hl=en&as_sdt=0,23

        headers = {
            "Accept": "application/json,text/*;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "User-Agent": ua.get_random_user_agent(),
        }
        # params = {"start": i, "q": "UMMZ+bird", "hl": "en", "as_sdt": "0, 23"}
        params = {"start": i, "q": "UMMZ+bird", "hl": "en", "as_sdt": "0, 23"}

        # response = umpy.http.get_resource(BASE_URL, params)
        response = requests.get(BASE_URL, params=params, headers=headers)

        print(response.request.headers)

        response.raise_for_status()  # if 200 returns None
        html = response.text

        soup = BeautifulSoup(html, "lxml")
        for result in soup.select(".gs_r.gs_or.gs_scl"):
            citation = {
                "title": result.select_one(".gs_rt").text,
                "title_url": select_value_by_key(result.select_one(".gs_rt a"), "href"),
                "pub_info": result.select_one(".gs_a").text,
                "snippet": result.select_one(".gs_rs").text,
                "cited_by": select_value_by_key(
                    result.select_one("#gs_res_ccl_mid .gs_nph+ a"), "href"
                ),
                "pdf_url": select_value_by_key(
                    result.select_one(".gs_or_ggsm a:nth-child(1)"), "href"
                ),
                # "related_articles": select_value_by_key(result.select_one("#gs_res_ccl_mid .gs_nph+ a+ a"), "href"),
            }
            citations.append(citation)

        # print(json.dumps(citations, indent=2, ensure_ascii=False))

        # print(f"HTML = {html}")

        # umpy.write.to_txt(
        #     f"./output/google_scholar-ummz-bird-{dt.now().strftime('%Y%m%dT%H%M')}.txt",
        #     [html],
        # )

        # citations.extend(
        #     [filter_data(doc, KEYS) for doc in response.json()["response"]["docs"]]
        # )
        # logger.info(f"{len(citations)} records retrieved")

        time.sleep(12)  # pause to confound rate limit

    # Write to file
    umpy.write.to_json(
        f"./output/google_scholar-ummz-bird-{dt.now().strftime('%Y%m%dT%H%M')}.json",
        citations,
    )

    # logger.info(f"Total articles retrieved = {len(articles)}")

    # End run
    logger.info(f"END RUN: {dt.now().isoformat()}")


if __name__ == "__main__":
    main(sys.argv[1:])  # ignore the first element (program name)
