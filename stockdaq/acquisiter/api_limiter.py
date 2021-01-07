"""Handle API limits.
"""
from configparser import ConfigParser

import pandas as pd


def api_selector(api_config_path, api_list, api_status_path="API.status"):
    """Selects an API based on availibility.

    Parameters
    ----------
    api_config_path: str
        Path to the API configuration file.
    api_list: list of str
        List of APIs, in preferred order.
    api_status_path: str, optional
        A path to store the API status.
        Defaults to "API.status"

    Returns
    -------
    api: str
        The available perferred API.
    """
    pass



def handle_api_limits(api_config_path, ):
    pass
