import os
import argparse
from configparser import ConfigParser


def parser():
    parser = argparse.ArgumentParser(description="Update StockDAQ database.")
    parser.add_argument(
        "-c", "--config", type=str,
        help="Configuration file. Use the -g/--get-config tag to get a"
        " sample configuration file",
        required=False
        )
    parser.add_argument(
        "-g", "--get-config", help="Get a sample configuration file.",
        action="store_true")
    parser.add_argument(
        "-ga", "--get-api-config", help="Get a sample API configuration file.",
        action="store_true"
    )
    return parser


def main(args=None):
    # config = ConfigParser(allow_no_value=True)
    options = parser().parse_args(args)
    if options.get_config or options.get_api_config:
        if options.get_config:
            make_sample_config()
        elif options.get_api_config:
            make_sample_api_config()
    else:
        import stockdaq.acquisiter.acquisiter
        import stockdaq.utils.config
        import stockdaq.symbol

        config = ConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read(options.config)

        stocklist_path = config["configuration"]["stock list"]
        stocklist = stockdaq.symbol.get_symbol_list(path=stocklist_path)

        api_config = ConfigParser(allow_no_value=True)
        api_config.optionxform = str
        api_config_path = config["configuration"]["API config"]
        api_config.read(api_config_path)

        apikey_dict = {}
        for section in api_config.sections():
            apikey_dict[section] = api_config[section]["API key"]
        # apikey_dict = dict(apikey_config["apikey"])

        api_list = stockdaq.utils.config.str2list(
            string=config["configuration"]["API list"]
            )

        frequency = config["configuration"]["frequency"]

        root_dir = config["configuration"]["rootdir"]

        file_structure = stockdaq.utils.config.str2list(
            string=config["configuration"]["file structure"]
            )

        rolling = config.getboolean("configuration", "rolling update")

        api_call_interval = config.getint(
            "configuration", "API calls interval (seconds)"
            )

        database_update_interval = config.getint(
            "configuration", "Database rolling update interval (seconds)"
            )

        ac = stockdaq.acquisiter.acquisiter.Acquisiter(
            stocklist=stocklist,
            apikey_dict=apikey_dict,
            api_list=api_list,
            api_config_path=api_config_path,
            frequency=frequency,
            root_dir=root_dir,
            file_structure=file_structure,
            rolling=rolling,
            api_call_interval=api_call_interval,
            database_update_interval=database_update_interval
            )

        download_kwargs = dict(config["download kwargs"])
        export_kwargs = dict(config["export kwargs"])

        ac.update_database(
            download_kwargs=download_kwargs, export_kwargs=export_kwargs,
            )


def make_sample_config():
    """Generate a sample config "config.ini".
    """
    path = "config.ini"
    if os.path.exists(path):
        raise FileExistsError("{} config exists.".format(path))
    else:
        config = ConfigParser(allow_no_value=True)
        config.optionxform = str
        config.add_section("configuration")
        config.set("configuration", "stock list", "stocklist.txt")
        config.set("configuration", "API config", "API_config.ini")
        config.set("configuration", "API list", "Alpha Vantage, yfinance")
        config.set("configuration", "frequency", "intraday")
        config.set("configuration", "rootdir", "./")
        config.set(
            "configuration", "file structure",
            "symbol, frequency, data"
            )
        config.set("configuration", "rolling update", "False")
        config.set("configuration", "API calls interval (seconds)", "1")
        config.set(
            "configuration", "Database rolling update interval (seconds)",
            "86400"
            )
        config.add_section("download kwargs")
        config.add_section("export kwargs")
        with open(path, "w") as f:
            config.write(f)


def make_sample_api_config():
    """Generate a sample API config "API_config.ini"
    """
    path = "API_config.ini"
    if os.path.exists(path):
        raise FileExistsError("{} config exists.".format(path))
    else:
        config = ConfigParser(allow_no_value=True)
        config.optionxform = str
        for api in ["Alpha Vantage", "yfinance"]:
            config.add_section(api)
            config.set(api, "API key", "")
            if api == "Alpha Vantage":
                config.set(api, "API requests per minute", "5")
                config.set(api, "API requests per day", "500")
            elif api == "yfinance":
                config.set(api, "API requests per minute", "12")
                config.set(api, "API requests per day", "1000")
            else:
                config.set(api, "API requests per minute", "1")
                config.set(api, "API requests per day", "100")
        with open(path, "w") as f:
            config.write(f)
