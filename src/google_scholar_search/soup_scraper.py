from bs4 import BeautifulSoup as soup, Tag
from citation import Citation
from scraper import Scraper


class SoupScraper(Scraper):
    def __init__(self, base_url: str, html: str) -> None:
        super().__init__(base_url, html)

    def __str__(self) -> str:
        return "BeautifulSoup scraper"

    # def get_author_links(self, url: str, tag: Tag) -> list:
    #     """Return author citation links from passed-in bs4.Tag object.

    #     Parameters:
    #         url (str): Citation URL
    #         html (bs4.Tag): Tag object

    #     Returns:
    #         list: sequence of author dictionaries
    #     """

    #     return [
    #         {"author_name": element.text, "url_fragment": f"{url}{element.get('href')}"}
    #         for element in tag.find_all("a", href=True)
    #     ]

    # def get_citation(self, url: str, tag: Tag) -> dict:
    #     """Return citation attributes from passed-in <url> and <html>.

    #     Parameters:
    #         url (str): Citation URL
    #         tag (BeautifulSoup.element.Tag): chunk of HTML

    #     Returns:
    #         dict: dictionary representation of a citation
    #     """

    #     return {
    #         "title": tag.select_one(".gs_rt").text,
    #         "title_url": self.select_value_by_key(tag.select_one(".gs_rt a"), "href"),
    #         "pub_info": tag.select_one(".gs_a").text,
    #         "author_links": self.get_author_links(url, tag.find("div", {"class": "gs_a"})),
    #         "snippet": tag.select_one(".gs_rs").text,
    #         "cited_by": self.select_value_by_key(
    #             tag.select_one("#gs_res_ccl_mid .gs_nph+ a"), "href"
    #         ),
    #         "pdf_url": self.select_value_by_key(
    #             tag.select_one(".gs_or_ggsm a:nth-child(1)"), "href"
    #         ),
    #         # "related_articles": select_value_by_key(result.select_one("#gs_res_ccl_mid .gs_nph+ a+ a"), "href"),
    #     }

    # def select_value_by_key(self, selector, key):
    #     """Return a value from a selector object.

    #     Parameters:
    #         selector (obj): selector object
    #         key (str): key to retrieve

    #     Returns:
    #         str: value associated with key
    #     """

    #     try:
    #         return selector[key]
    #     except (KeyError, TypeError):
    #         return None

    def scrape(self):
        """TODO"""

        return [
            Citation(self.base_url, tag).to_dict()
            # self.get_citation(self.base_url, tag)
            for tag in soup(self.html, "lxml").select(".gs_r.gs_or.gs_scl")
        ]
