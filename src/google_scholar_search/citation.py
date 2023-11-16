from dataclasses import dataclass, asdict


@dataclass
class Citation:
    """TODO"""

    title: str
    title_url: str
    pub_info: str
    author_links: list[dict]
    snippet: str
    cited_by: str
    pdf_url: str
    # related_articles: str

    def to_dict(self):
        """Return Citation as a dictionary."""
        return asdict(self)
