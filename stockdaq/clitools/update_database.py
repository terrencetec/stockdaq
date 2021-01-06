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
    return parser


def main(args=None):
    # config = ConfigParser(allow_no_value=True)
    options = parser().parse_args(args)
    if options.get_config:
        make_sample_config()
    else:
        import stockdaq.acquisiter.acquisiter
        import stockdaq.utils.config
        import stockdaq.symbol

        config = ConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read(options.config)

        stocklist_path = config["configuration"]["stock list"]
        stocklist = stockdaq.symbol.get_symbol_list(path=stocklist_path)

        apikey_config = ConfigParser(allow_no_value=True)
        apikey_config.optionxform = str
        apikey_config.read(config["configuration"]["api key"])
        apikey_dict = dict(apikey_config["apikey"])

        api_list = stockdaq.utils.config.str2list(
            string=config["configuration"]["api list"]
            )

        frequency = config["configuration"]["frequency"]

        root_dir = config["configuration"]["rootdir"]

        file_structure = stockdaq.utils.config.str2list(
            string=config["configuration"]["file structure"]
            )

        ac = stockdaq.acquisiter.acquisiter.Acquisiter(
            stocklist=stocklist,
            apikey_dict=apikey_dict,
            api_list=api_list,
            frequency=frequency,
            root_dir=root_dir,
            file_structure=file_structure,
            )

        download_kwargs = dict(config["download kwargs"])
        export_kwargs = dict(config["export kwargs"])
        ac.update_database(download_kwargs, export_kwargs)


def make_sample_config():
    import os

    path = "config.ini"
    if os.path.exists(path):
        raise FileExistsError("{} config exists.".format(path))
    else:
        config = ConfigParser(allow_no_value=True)
        config.optionxform = str
        config.add_section("configuration")
        config.set("configuration", "stock list", "stocklist.txt")
        config.set("configuration", "api key", "apikey")
        config.set("configuration", "api list", "Alpha Vantage, yfinance")
        config.set("configuration", "frequency", "intraday")
        config.set("configuration", "rootdir", "./")
        config.set(
            "configuration", "file structure",
            "symbol, frequency, data"
            )
        config.add_section("download kwargs")
        config.add_section("export kwargs")
        with open(path, "w") as f:
            config.write(f)
