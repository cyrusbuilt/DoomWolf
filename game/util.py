import os


def str_to_bool(val: str) -> bool:
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    if val.lower() in ('y', 'yes', 't', 'true', 'on', '1'):
        return True

    if val.lower() in ('n', 'no', 'f', 'false', 'off', '0'):
        return False

    raise ValueError(f"Invalid truth value: {val}")


def get_user_home() -> str:
    return os.path.expanduser('~')


def get_user_game_data_path() -> str:
    return os.path.join(get_user_home(), '.doom_wolf')
