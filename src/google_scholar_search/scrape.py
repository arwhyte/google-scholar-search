from bs4 import Tag


def retrieve_author_links(base_url: str, tag: Tag) -> list:
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


def retrieve_citation(base_url, html) -> dict:
    """Return citation attributes from passed-in <url> and <html>.

    Parameters:
        base_url (str): Base URL of citation
        html (BeautifulSoup.element.Tag): chunk of HTML

    Returns:
        dict: dictionary representation of a citation
    """

    return {
        "title": html.select_one(".gs_rt").text,
        "title_url": select_value_by_key(html.select_one(".gs_rt a"), "href"),
        "pub_info": html.select_one(".gs_a").text,
        "author_links": retrieve_author_links(base_url, html.find("div", {"class": "gs_a"})),
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
