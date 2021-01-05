"""Download data and save as Pandas dataframe using APIs.
"""
import os

import pandas as pd


class Downloader:
    """
    """
    def __init__(self, api, apikey=None, output_format="pandas"):
        """
        """
        self.api = api
        self.apikey = apikey
        self.output_format = output_format

    def download(self, stock_symbol, date,):
        if api in ["av", "AV", "Av", "alpha vantage",
                   "Alpha Vantage", "Alpha vantage",
                   "alpha_vantage", "Alpha_Vantage",]:
            from alpha_vantage.timeseries import TimeSeries
            ts = TimeSeries(key=apikey)
