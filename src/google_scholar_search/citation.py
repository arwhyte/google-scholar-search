from bs4 import Tag


class Citation:
    """TODO"""

    def __init__(self, url: str, tag: Tag) -> None:
        """TODO"""
        self.url = url
        self.tag = tag

        self.title = tag.select_one(".gs_rt").text
        self.title_url = self.__select_value_by_key(tag.select_one(".gs_rt a"), "href")
        self.pub_info = tag.select_one(".gs_a").text
        self.author_links = self.__get_author_links(url, tag.find("div", {"class": "gs_a"}))
        self.snippet = tag.select_one(".gs_rs").text
        self.cited_by = self.__select_value_by_key(
            tag.select_one("#gs_res_ccl_mid .gs_nph+ a"), "href"
        )
        self.pdf_url = self.__select_value_by_key(
            tag.select_one(".gs_or_ggsm a:nth-child(1)"), "href"
        )
        # self.related_articles = self.select_value_by_key(tag.select_one("#gs_res_ccl_mid .gs_nph+ a+ a"), "href")

    def __str__(self) -> str:
        return "Citation"

    # def select(self) -> None:
    #     """TODO"""

    #     self.title: str = self.tag.select_one(".gs_rt").text
    #     self.title_url: str = self.__select_value_by_key(self.tag.select_one(".gs_rt a"), "href")
    #     self.pub_info: str = self.tag.select_one(".gs_a").text
    #     self.author_links: list[dict] = self.__get_author_links(
    #         self.url, self.tag.find("div", {"class": "gs_a"})
    #     )
    #     self.snippet: str = self.tag.select_one(".gs_rs").text
    #     self.cited_by: str = self.__select_value_by_key(
    #         self.tag.select_one("#gs_res_ccl_mid .gs_nph+ a"), "href"
    #     )
    #     self.pdf_url: str = self.__select_value_by_key(
    #         self.tag.select_one(".gs_or_ggsm a:nth-child(1)"), "href"
    #     )

    def __get_author_links(self, url: str, tag: Tag) -> list:
        """Return author citation links from passed-in bs4.Tag object.

        Parameters:
            url (str): Citation URL
            html (bs4.Tag): Tag object

        Returns:
            list: sequence of author dictionaries
        """

        return [
            {"author_name": element.text, "url_fragment": f"{url}{element.get('href')}"}
            for element in tag.find_all("a", href=True)
        ]

    def __select_value_by_key(self, selector, key):
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

    def to_dict(self):
        """Return citation attributes as a dictionary.

        Parameters:
            None

        Returns:
            dict: dictionary representation of a citation
        """

        # return vars(self) # includes tag and url

        return {
            "title": self.title,
            "title_url": self.title_url,
            "pub_info": self.pub_info,
            "author_links": self.author_links,
            "snippet": self.snippet,
            "cited_by": self.cited_by,
            "pdf_url": self.pdf_url,
        }
