"""Alpha Vantage downloader
"""

import alpha_vantage.timeseries
import numpy as np
import pandas as pd

import stockdaq.constants
import stockdaq.data.downloader
import stockdaq.data.manager


class AlphaVantageDownloader(stockdaq.data.downloader.Downloader):
    """
    """
    def __init__(self, apikey, output_format="pandas"):
        """
        """
        super().__init__(
            api="Alpha Vantage")
        self.apikey = apikey
        self.output_format = output_format
        self.ts = alpha_vantage.timeseries.TimeSeries(
            key=self.apikey, output_format=self.output_format)

    def get_intraday(self, symbol, interval="1min", outputsize="full"):
        """Get intraday data, set self.dataframe

        Parameters
        ----------
        symbol: str
            Stock symbol
        interval: str, optional.
            Interval between data.
            Defaults to "1min".
            Options are ["1min", "5min", "15min", "30min", "60min"].
        outputsize: str, optional.
            Defaults to "full".
            Options are ["compact", "full"].
            "compact" only returns last 100 data points.
            "full" returns full-length intraday times.

        Returns
        -------
        pandas.core.frame.DataFrame
            The intraday data.
        """
        self.rawdata, _ = self.ts.get_intraday(
            symbol=symbol, interval=interval, outputsize=outputsize)
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

        open_ = dataframe["1. open"].values
        high = dataframe["2. high"].values
        low = dataframe["3. low"].values
        close = dataframe["4. close"].values
        volume = dataframe["5. volume"].values

        dataframe = pd.DataFrame(
            data=np.array([open_, high, low, close, volume]).T,
            columns=stockdaq.constants.columns,
            index=dt)

        return dataframe
