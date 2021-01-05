"""Download data and save as Pandas dataframe using APIs.
"""
import os

import pandas as pd

import stockdaq.data.manager


class Downloader:
    """
    """
    def __init__(self, api):
        """
        """
        self.api = api
        self.dataframe = None

    def export(self, criterion="date", prefix="", suffix="",
            extension=".h5", conflict="merge", mergehow="keep old"):
        """Export self.dataframe to hdf5 files, names derive from criterion.

        Parameters
        ----------
        criterion: str, optional
            Data in same file has same "date", "month", or "year".
            Defaults to date.
        prefix: str, optional
            Prefix to the filename.
        suffix: str, optional
            suffix to the filename, before the extension.
        extension: str, optional
            Extension of the files.
            Defaults to ".h5".
        conflict: str, optional
            How to resolve conflicts.
            options are ["merge", "overwrite", "ignore"].
            "merge": append non-duplicating data to the existing datafile.
            "overwrite": replace the existing file.
            "ignore": don't do anything.
        mergehow: str, optional
            Only effective when conflict == "merge".
            "keep old": If there are duplicated indexes, keep old data.
            "update": If there are duplicated indexes, keep new data.
        """
        if criterion == "date":
            data_dict = stockdaq.data.manager.segmenter(
                dataframe=self.dataframe,
                criterion=criterion,
                )
        for key in data_dict.keys():
            data = data_dict[key]
            filename = prefix+key+suffix+extension
            data.save(
                path=filename, format="hdf5", conflict=conflict,
                mergehow=mergehow
                )
