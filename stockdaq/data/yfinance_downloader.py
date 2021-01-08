"""yfinance downloader
"""

import numpy as np
import pandas as pd
import yfinance

import stockdaq.constants
import stockdaq.data.downloader
import stockdaq.data.manager


class yfinanceDownloader(stockdaq.data.downloader.Downloader):
    """Downloader using yfinance

    Attributes
    ----------
    dataframe: pandas.core.frame.DataFrame
        The obtained data. Update using getters.
    """
    def __init__(self, apikey=""):
        """Constructor

        Parameters
        ----------
        apikey: str
            Dummy keyholder
        """
        super().__init__(api="yfinance")

    def download(self, symbol, frequency="intraday", **kwargs):
        """Get data from API

        Parameters
        ----------
        symbol: str
            Stock symbol
        frequency: str, optional
            "intraday", "daily", "weekly", "monthly".
        **kwargs:
            Keyword arguments passed to the getter methods.
        """
        self.get_data(
            symbol=symbol, frequency=frequency,
            yfinance_download_kwargs=kwargs
            )

    def get_data(
            self, symbol, frequency="intraday", yfinance_download_kwargs={}):
        """Get intraday data, set self.dataframe

        Parameters
        ----------
        symbol: str
            Stock symbol
        frequency: str, optional
            "intraday", "daily", "weekly", "monthly".
        yfinance_download_kwargs: dict, optional
            Keyword arguments that passes to yfinance.download()

        Returns
        -------
        pandas.core.frame.DataFrame
            The intraday data.
        """
        period = "max"
        if frequency == "intraday":
            interval = "1m"
            period = "7d"
        elif frequency == "daily":
            interval = "1d"
        elif frequency == "weekly":
            interval = "1wk"
        elif frequency == "monthly":
            interval = "1mo"
        else:
            raise ValueError("{} frequency not available".format(frequency))

        self.rawdata = yfinance.download(
            tickers=symbol, interval=interval, period=period,
            **yfinance_download_kwargs
            )
        self.dataframe = self.formatter(datadump=self.rawdata)
        return self.dataframe

    def formatter(self, datadump):
        """Convert Alpha Vantage dataframe to standard stockdaq format

        Parameters
        ----------
        datadump: pandas.core.frame.DataFrame
            Dataframe from Alpha Vantage.

        Returns
        -------
        dataframe: pandas.core.frame.DataFrame
            Formated dataframe.
        """
        # Sort by ascending datetime
        dataframe = datadump.sort_index()

        # Remove timezone
        dt = []
        for i in range(len(dataframe.index)):
            dt.append(dataframe.index[i].replace(tzinfo=None))
        dt = pd.DatetimeIndex(dt)

        open_ = dataframe["Open"].values
        high = dataframe["High"].values
        low = dataframe["Low"].values
        close = dataframe["Close"].values
        volume = dataframe["Volume"].values

        dataframe = pd.DataFrame(
            data=np.array([open_, high, low, close, volume]).T,
            columns=stockdaq.constants.columns,
            index=dt)

        return dataframe
