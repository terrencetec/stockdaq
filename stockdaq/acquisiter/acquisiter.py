"""Data acquisition system.
"""
import datetime
import os
import sys
import time

import stockdaq.data.downloader_dict
from stockdaq.logger import logger


class Acquisiter:
    """Data Acquisiter

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
    file_structure: list of str, optional
        How to set up parent/child folders.
        Defaults to ["symbol", "frequency", "data"].

    Attributes
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
    file_structure: list of str, optional
        How to set up parent/child folders.
        Defaults to ["symbol", "frequency", "data"].
    """
    def __init__(self, stocklist, api_config_path, apikey_dict,
            api_list=["Alpha Vantage",],frequency="intraday", root_dir="./",
            file_structure=["symbol", "frequency", "data"],
            rolling=False, api_call_interval=12,
            database_update_interval=86400):
        """Constructor

        Parameters
        ----------
        stocklist: list of str
            List of symbols of stocks of interest.
        api_config_path: str
            Path to the API configuration file.
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
        file_structure: list of str, optional
            How to set up parent/child folders.
            Defaults to ["symbol", "frequency", "data"].
        rolling: boolean, optional
            Rolling update. Rate limited by API requestion limitations
            set in the API configuration file.
            Defaults to be False.
        api_call_interval: int, optional
            Minimal delay (seconds) between API calls.
            Use your API's limitation to derive this value.
            Defaults to 12.
        database_update_interval: int, optional
            Interval (seconds) between each database update.
            Defaults to 86400 (1 day).
        """
        self.stocklist = stocklist
        self.root_dir = root_dir
        self.api_config_path = api_config_path
        self.api_list = api_list
        self.apikey_dict = apikey_dict
        self.frequency = frequency
        self.file_structure = file_structure
        self.rolling = rolling
        self.api_call_interval = datetime.timedelta(seconds=api_call_interval)
        self.database_update_interval = datetime.timedelta(
            seconds=database_update_interval)

    def update_database(self, download_kwargs={}, export_kwargs={}):
        """Get stock data from API and update datebase.

        Parameters
        ----------
        downloader_kwargs: dict
            Keyword arguments passed to
            stockdaq.data.downloader.YourDownloader.download() method.
        export_kwargs: dict
            Keyword arguments passed to
            stockdaq.data.downloader.Downloader.export() method.
        """
        # api = self.api_list[0]
        # apikey = self.apikey_dict[api]
        # downloader = stockdaq.data.downloader_dict.downloader_dict[api](
        #     apikey=apikey
        #     )
        last_update_datetime = datetime.datetime.now()

        for symbol in self.stocklist:
            for api in self.api_list:
                try:
                    apikey = self.apikey_dict[api]
                    downloader = (
                        stockdaq.data.downloader_dict.downloader_dict[api](
                            apikey=apikey
                            )
                        )
                    downloader.download(
                        symbol=symbol, frequency=self.frequency,
                        **download_kwargs
                        )
                    last_api_call_datetime = datetime.datetime.now()

                    # Now prefix is the dir.
                    prefix = self.get_prefix(symbol=symbol)
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

                    while (datetime.datetime.now() - last_api_call_datetime <
                           self.api_call_interval):
                        time.sleep(1)
                    break  # Break out of the api loop when success
                except ValueError as err:
                    logger.error("Error encountered when trying to acquisite "
                                 "symbol: {} data from API: {}\nError message:"
                                 "\n{}"
                                 "".format(symbol, api, err))
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise

        logger.info("Database update finished.")

        if self.rolling:
            next_update_datetime = (last_update_datetime
                                    + self.database_update_interval)
            logger.info("Rolling update enabled, "
                        "next update is scheduled at "
                        "{}.".format(str(next_update_datetime)))
            while datetime.datetime.now() < next_update_datetime:
                time.sleep(1)
            self.update_database(
                download_kwargs=download_kwargs, export_kwargs=export_kwargs
                )

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
