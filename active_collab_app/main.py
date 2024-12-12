import argparse
import configparser
import http.client as http_client
import json
import logging
import os
import sys
import time
from collections.abc import Iterator

from active_collab_api.active_collab import ActiveCollab
from active_collab_app import CFG_SECTION_DEFAULT
from active_collab_app.delete import run_delete_all
from active_collab_app.dump import run_dump_all
from active_collab_app.empty import run_empty_trash
from active_collab_app.html import run_html
from active_collab_app.info import run_info
from active_collab_app.load import run_load_all
from active_collab_app.testing import run_testing
from active_collab_app.verify import run_verify_all
from active_collab_app.version import run_version


def setup_logging(log_level=logging.ERROR, http_debugging=False) -> None:
    root = logging.getLogger()
    root.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)
    if http_debugging:
        # These two lines enable debugging at httplib level (requests->urllib3->http.client)
        http_client.HTTPConnection.debuglevel = 1


def load_config(args) -> configparser.ConfigParser:
    if not os.path.exists(args.config):
        raise FileNotFoundError(f"Configfile '{args.config}' not found!")
    config = configparser.ConfigParser(interpolation=None)
    config.read(args.config)
    return config


def serialize_output(output) -> str:
    # serialize the output
    return json.dumps(output, indent=4)


def login(config: configparser.ConfigParser) -> ActiveCollab:
    # create the AC Client
    base_url = config.get(CFG_SECTION_DEFAULT, "base_url")
    is_cloud = config.getboolean(CFG_SECTION_DEFAULT, "is_cloud", fallback=False)
    account = ""
    if is_cloud:
        account = config.get("LOGIN", "account", fallback="")
    ac = ActiveCollab(base_url, is_cloud)
    ac.login(config.get("LOGIN", "username"), config.get("LOGIN", "password"), account)
    return ac


def run(args, config: configparser.ConfigParser):  # pylint: disable=R0911
    # run the commands
    if args.command == "version":
        return run_version()
    if args.command == "info":
        return run_info(login(config), config)
    if args.command == "dump":
        return run_dump_all(login(config), config)
    if args.command == "delete":
        return run_delete_all(login(config), config)
    if args.command == "empty":
        return run_empty_trash(login(config), config)
    if args.command == "verify":
        return run_verify_all(login(config), config)
    if args.command == "load":
        return run_load_all(login(config), config)
    if args.command == "testing":
        return run_testing(login(config), config)
    if args.command == "html":
        return run_html(config)
    return None


def arg_parser() -> (dict, argparse.ArgumentParser):
    # parse arguments
    parser = argparse.ArgumentParser(
        prog="acdump",
        description="This is a tool to dump data from Active-Collab",
        epilog="(c) 2024 by ACME VC, Charlie Sloan <cs@example.com>",
    )
    parser.add_argument(
        "-c", "--config", required=True, help="use the named config file"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable some move verbose output"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument(
        "--http-debug", action="store_true", help="Enable HTTP debug output"
    )
    parser.add_argument(
        "command",
        choices=[
            "version",
            "info",
            "dump",
            "delete",
            "empty",
            "verify",
            "load",
            "testing",
            "html",
        ],
        help="The command to run",
    )
    args = parser.parse_args()
    return args, parser


def main() -> None:
    args, parser = arg_parser()
    config = load_config(args)
    log_level = logging.ERROR
    if args.verbose:
        log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    setup_logging(log_level, args.http_debug)

    t_start = time.time()
    logging.info("Started")
    output = run(args, config)
    if output is None:
        parser.print_help()

    if isinstance(output, Iterator):
        output = list(output)
    if output is not None:
        print(serialize_output(output))
    logging.info("Finished after %0.3f seconds" % (time.time() - t_start))


if __name__ == "__main__":
    main()
