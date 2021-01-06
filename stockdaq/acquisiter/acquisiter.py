"""Data acquisition system.
"""
import os

import stockdaq.data.downloader_dict


class Acquisiter:
    """
    """
    def __init__(self, stocklist, apikey_dict, api_list=["Alpha Vantage",],
            frequency="intraday", root_dir="./",
            file_structure=["symbol", "frequency", "data"]):
        """Constructor

        Parameters
        ----------
        stocklist: list of str
            List of symbols of stocks of interest.
        apikey_dict: dict
            A dictionary of API keys in {"api":"key"} pairs.
        api_list: list of str, optional
            List of APIs, in preferred order.
            Options are ["Alpha Vantage",]
        root_dir: str, optional
            The root directory of the database.
        frequency: str, optional
            "intraday", "daily", "weekly", "monthly"
            Options are ["intraday"].
        """
        self.stocklist = stocklist
        self.root_dir = root_dir
        self.api_list = api_list
        self.apikey_dict = apikey_dict
        self.frequency = frequency
        self.file_structure = file_structure

    def update_database(self, download_kwargs={}, export_kwargs={}):
        """Get stock data from API and update datebase.
        """
        api = self.api_list[0]
        apikey = self.apikey_dict[api]
        downloader = stockdaq.data.downloader_dict.downloader_dict[api](
            apikey=apikey
            )
        for symbol in self.stocklist:
            downloader.download(
                symbol=symbol, frequency=self.frequency, **download_kwargs
                )

            prefix = self.get_prefix(symbol=symbol)  # Now prefix is the dir.
            if not os.path.isdir(prefix):
                os.makedirs(prefix)

            # Now add the customized prefix
            try:
                export_kwargs["prefix"]
            except KeyError:
                export_kwargs["prefix"] = None

            if export_kwargs["prefix"] is not None:
                prefix += export_kwargs["prefix"]

            new_export_kwargs = dict(export_kwargs)
            new_export_kwargs["prefix"] = prefix
            downloader.export(**new_export_kwargs)

    def get_prefix(self, symbol):
        """Get path prefix for a specific data.

        Parameters
        ----------
        symbol: str
            The stock symbol.

        Returns
        -------
        prefix: str
            The prefix of the file path.
        """
        prefix = self.root_dir+""
        for folder in self.file_structure:
            if folder == "data":
                break
            elif folder == "frequency":
                prefix += self.frequency+"/"
            elif folder == "symbol":
                prefix += symbol+"/"
            else:
                raise ValueError("{} structure not available.".format(folder))
        return prefix
