"""Library for handling stock symbols.
"""
import os
import csv

import numpy as np


def make_symbol_list(
        input_path, output_path, overwrite=True, omit=["^", "."],
        has_header=True, symbol_index=0):
    """Make a list of stock symbols from the nasdaq companylist.csv file.

    Parameters
    ----------
    input_path: str
        The path of the companylist.csv file.
    output_path: str
        The output path.
    overwrite: boolean, optional
        If the output path exists, overwrite.
        Defaults to True.
    omit: list of str, optional
        If the stock symbol contains characters in this list, it will be
        ignored. For example, "AL^A" will be ignored.
        Defaults to ["^", "."].
    has_header: boolean, optional
        If the csv file has header indicating the column of symbols.
    symbol_index: int, optional
        The column of the symbols, if the header doesn't indicate.
    """
    with open(input_path, "r") as csvfile:
        data = csv.reader(csvfile)
        data = list(data)
        if has_header:
            header = data[0]
            symbol_index = header.index('Symbol')
            symbol_list = np.array(data)[1:, symbol_index]
        else:
            symbol_list = np.array(list(data))[:, symbol_index]

    if os.path.exists(output_path) and not overwrite:
        raise FileExistsError("File {} already exists".format(output_path))

    symbol_list.sort()

    with open(output_path, "w") as f:
        for symbol in symbol_list:
            if any([char in symbol for char in omit]):
                pass
            else:
                f.write("{}\n".format(symbol))


def get_symbol_list(path, omit=["^", "."]):
    """Read a file of symbols list and return a list of symbols

    Parameters
    ----------
    path: str
        Path to the list of symbols. The file should contain newline
        separated strings of symbols.
    omit: list of str, optional
        If the stock symbol contains characters in this list, it will be
        ignored. For example, "AL^A" will be ignored.
        Defaults to ["^", "."].

    Returns
    -------
    symbol_list: list of str
        The list of stock symbols.
    """
    with open(path, "r") as f:
        symbol_list = f.readlines()
    symbol_list = [symbol.rstrip('\n') for symbol in symbol_list]

    remove_list = []
    for symbol in symbol_list:
        for char in omit:
            if char in symbol:
                if symbol not in remove_list:
                    remove_list.append(symbol)
    for remove_symbol in remove_list:
        symbol_list.remove(remove_symbol)
    return symbol_list
