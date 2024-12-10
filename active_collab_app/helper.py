import configparser


def map_user_id(config: configparser.ConfigParser, from_user_id: int) -> int:
    option_name = f"map_user_id_{from_user_id}"
    if config.has_option("DEFAULT", option_name):
        return config.getint("DEFAULT", option_name)
    return from_user_id
