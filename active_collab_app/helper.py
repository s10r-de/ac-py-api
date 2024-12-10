import configparser

from active_collab_app import CFG_SECTION_DEFAULT


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
