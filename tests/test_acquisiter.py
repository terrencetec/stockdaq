import os
import shutil

import stockdaq.acquisiter.acquisiter as ac


def test_acquisiter():
    stocklist = ["AAPL", "AMD"]
    api_config_path = ""
    apikey_dict = {"Alpha Vantage": "123"}
    root_dir = "tests/data/"
    for symbol in stocklist:
        if os.path.exists(root_dir+symbol):
            shutil.rmtree(root_dir+symbol)
    a = ac.Acquisiter(
        stocklist, api_config_path, apikey_dict,
        api_list=["Alpha Vantage",],frequency="intraday", root_dir=root_dir,
        file_structure=["symbol", "frequency", "data"],
        rolling=False, api_call_interval=1,
        database_update_interval=86400
        )
    a.update_database()
    flag = all([os.path.exists("tests/data/{}".format(symbol))
               for symbol in stocklist])
    for symbol in stocklist:
        if os.path.exists(root_dir+symbol):
            shutil.rmtree(root_dir+symbol)
    assert flag
