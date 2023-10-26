import argparse as ap


def create_parser(name: str) -> ap.ArgumentParser:
    """Create, name, and return a parser object.

    Parameters:
        name (str): the name of the parser

    Parser arguments:
        short_flag (str): short version of command option
        long_flag (str): long version of command option
        type (str): argument type (e.g., str, int, bool)
        required (bool): specifies whether or not command option is required
        default (obj): default value, typically str or int
        help (str): short description of command option

    Returns:
        parser (ap.ArgumentParser): a parser object
    """

    parser: ap.ArgumentParser = ap.ArgumentParser(
        prog=name,
        description="Welcome to %(prog)s! We're here to help you scavenge your specimens.",
        epilog="Thanks for using %(prog)s! Have a great day!",
        usage="%(prog)s [options]",
    )
    parser.add_argument(
        "-p",
        "--plugin",
        type=str,
        required=True,
        help="Web scraper plugin module",
    )
    parser.add_argument(
        "-o",
        "--offset",
        type=int,
        required=False,
        default=0,
        help="The start page.",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        required=False,
        default=1,
        help="The number of pages to return.",
    )
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        required=True,
        help="The query string with which to search Google Scholar.",
    )
    return parser
