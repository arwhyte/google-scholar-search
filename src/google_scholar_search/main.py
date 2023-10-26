import cli_arg_parser as ap
import importlib as il
import importlib.util as ilu
import sys

from types import ModuleType


def import_module(module_name: str, package_name: str | None = None) -> ModuleType:
    """TODO"""
    absolute_name = ilu.resolve_name(module_name, package_name)
    if ilu.find_spec(f"{absolute_name}", package_name):
        return il.import_module("plugins.scraperapi")
    else:
        raise ModuleNotFoundError(f"{absolute_name} not located", name=absolute_name)


def main(args):
    """TODO"""

    parser = ap.create_parser("Web Scraper")
    cli_args = parser.parse_args(args)
    plugin_name: str = cli_args.plugin

    match plugin_name:
        case "scraperapi":
            plugin = import_module("scraperapi", "plugins")
        case "serpapi":
            plugin = import_module("serpapi", "plugins")
        case _:
            raise ModuleNotFoundError(f"Error: {plugin_name} module not located", name=plugin_name)

    # Test the plugin
    scraper = plugin.Scraper()
    print(scraper)


if __name__ == "__main__":
    main(sys.argv[1:])
