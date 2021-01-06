"""Utilities for configparser.
"""

def str2list(string):
    """Convert a string with comma separated elements to a python list.

    Parameters
    ----------
    string: str
        A string with comma with comma separated elements

    Returns
    -------
    list
        A list.
    """
    string_list = [str_.rstrip(" ").lstrip(" ") for str_ in string.split(",")]
    return string_list
