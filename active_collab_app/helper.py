import configparser
from datetime import datetime
import time

from active_collab_app import CFG_OPTION_DUMP_TIMESTAMP_FILE, CFG_SECTION_DEFAULT


def map_user_id(config: configparser.ConfigParser, from_user_id: int) -> int:
    option_name = f"map_user_id_{from_user_id}"
    if config.has_option(CFG_SECTION_DEFAULT, option_name):
        return config.getint(CFG_SECTION_DEFAULT, option_name)
    return from_user_id


def check_is_cloud(config: configparser.ConfigParser) -> bool:
    is_cloud = config.getboolean(CFG_SECTION_DEFAULT, "is_cloud", fallback=False)
    if is_cloud is False:
        base_url = config.get(CFG_SECTION_DEFAULT, "base_url")
        if base_url.startswith("https://activecollab.com"):
            is_cloud = True
    return is_cloud


def map_company_id(config: configparser.ConfigParser, from_company_id: int) -> int:
    option_name = f"map_company_id_{from_company_id}"
    if config.has_option(CFG_SECTION_DEFAULT, option_name):
        return config.getint(CFG_SECTION_DEFAULT, option_name)
    return from_company_id


def save_dump_timestamp(config: configparser.ConfigParser) -> str:
    filename = config.get(CFG_SECTION_DEFAULT, CFG_OPTION_DUMP_TIMESTAMP_FILE)
    ts = datetime.now().isoformat()
    with open(filename, "w", encoding="ascii") as fh:
        fh.write(f"{ts}")
    return filename


def format_timestamp_as_date(ts: int) -> str:
    time_format = "%Y-%m-%d"
    return time.strftime(time_format, time.gmtime(ts))

def format_timestamp_as_datetime(ts: int) -> str:
    time_format = "%Y-%m-%d %H:%M:%S"
    return time.strftime(time_format, time.gmtime(ts))
