"""Base data class
"""
import os

import numpy as np
import pandas as pd

import stockdaq.constants
import stockdaq.data.data
from stockdaq.logger import logger


header = stockdaq.constants.columns

class Data:
    """Data class for saving and loading stockdaq format stock data.

    Parameters
    ----------
    datetime_column: pandas.core.indexes.datetimes.DatetimeIndex
        Date and time
    open_: array
        open price data
    high: array
        high price data
    low: array
        low price data
    close: array
        close price data
    volume: array
        volume data

    Attritubes
    ----------
    datetime_column: pandas.core.indexes.datetimes.DatetimeIndex
        Date and time
    open_: array
        open price data
    high: array
        high price data
    low: array
        low price data
    close: array
        close price data
    volume: array
        volume data
    dataframe: pandas.core.frame.DataFrame
        The data frame.
    """
    def __init__(
            self, datetime_column=None, open_=None, high=None, low=None,
            close=None, volume=None, dataframe=None, load_path=None):
        """Initization with data array or dataframe.

        Parameters
        ----------
        datetime_column: pandas.core.indexes.datetimes.DatetimeIndex
            Date and time
        open_: array
            open price data
        high: array
            high price data
        low: array
            low price data
        close: array
            close price data
        volume: array
            volume data
        dataframe: pandas.core.frame.DataFrame
            dataframe
        load_path: str
            file name of a stockdaq data file.

        Note
        ----
        Only specify data in stockdaq standardized format.
        """
        self.dataframe = None
        if (any([datetime_column is None, open is None,
                high is None, low is None,
                close is None, volume is None]) and
                dataframe is None and load_path is None):
            raise ValueError("Missing data.")
        elif all([datetime_column is not None, open is not None,
                high is not None, low is not None,
                close is not None, volume is not None]):
            self.datetime_column = datetime_column
            self.open = open_
            self.high = high
            self.low = low
            self.close = close
            self.volume = volume
            self._set_self_dataframe_from_data()
        elif load_path is not None:
            self.load(load_path)
        elif dataframe is not None:
            self.dataframe = dataframe
            self._set_self_data_from_dataframe()

    def save(self, path, format="hdf5", conflict="merge",
            mergehow="keep old", **kwargs):
        """Save the dataframe

        Parameters
        ----------
        path: str
            The path to be saved to.
        format: str, optional
            The format of the file to be saved.
            Defaults to "hdf5".
            Options are ["hdf5", "csv"]
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
        **kwargs:
            Keyword arguments passed to the pandas methods
        """
        if os.path.exists(path) and conflict=="ignore":
            logger.info("{} exists, ignoring.".format(path))
            return None
        elif os.path.exists(path) and conflict=="overwrite":
            logger.info("{} exists, overwriting.".format(path))
        elif os.path.exists(path) and conflict=="merge":
            logger.info("{} exists, merging. How: {}".format(path, mergehow))
            self.merge(path=path, mergehow=mergehow)
        elif os.path.exists(path):
            raise ValueError("conflict: {} not available.".format(conflict))

        if format == "hdf5":
            self.dataframe.to_hdf(
                path_or_buf=path, key="stockdaq", mode="w", **kwargs)
        elif format == "csv":
            self.dataframe.to_csv(path_or_buf=path, header=header, **kwargs)
        else:
            raise ValueError("{} format not available".format(format))
        logger.info("Data written to path: {}".format(path))

    def load(self, path, format="hdf5"):
        """Load a single stockdaq data file.

        Parameters
        ----------
        path: str
            The path of the file to be read.
        format: str, optional
            The format of the file to be saved.
            Defaults to "hdf5".
            Options are ["hdf5", "csv"]
        """
        if not os.path.exists(path):
            raise FileExistsError("{} does not exist".format(path))

        if format == "hdf5":
            self.dataframe = pd.read_hdf(path)
        elif format == "csv":
            self.dataframe = pd.read_csv(path, index_col=0)
        else:
            raise ValueError("{} format not available".format(format))

        self._set_self_data_from_dataframe()

    def merge(self, path, mergehow="keep old"):
        """Merge self.dataframe with an exist datafile.

        Parameters
        ----------
        path: str
            The path of the file to be merged.
        mergehow: str, optional
            "keep old": If there are duplicated indexes, keep old data.
            "update": If there are duplicated indexes, keep new data.
        """
        data = stockdaq.data.data.Data(load_path=path)
        if mergehow == "keep old":
            df_keep = data.dataframe
            df_other = self.dataframe
        elif mergehow == "update":
            df_keep = self.dataframe
            df_other = data.dataframe
        else:
            raise ValueError("mergehow:{} not available".format(mergehow))
        df = pd.concat([df_keep, df_other])
        df = df[~df.index.duplicated()]
        df = df.sort_index()
        self.dataframe = df

    def _set_self_data_from_dataframe(self):
        """ set self.open, self.close, etc from self.dataframe.
        """
        self.datetime_column = pd.DatetimeIndex(self.dataframe.index)
        self.open = self.dataframe["open"].values
        self.high = self.dataframe["high"].values
        self.low = self.dataframe["low"].values
        self.close = self.dataframe["close"].values
        self.volume = self.dataframe["volume"].values

    def _set_self_dataframe_from_data(self):
        """ set self.dataframe from self.open, self.close, etc.
        """
        self.dataframe = pd.DataFrame(
            data=np.array(
                [self.open, self.high, self.low, self.close, self.volume]
                ).T,
            index=self.datetime_column,
            columns=header,
            )
