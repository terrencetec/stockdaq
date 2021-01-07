import stockdaq.data.data

def test_data():
    data = stockdaq.data.data.Data(
        load_path="tests/data/TSLA/intraday/2020-12-24.h5")
    data.merge(path="tests/data/TSLA/intraday/2020-12-28.h5")
    data._set_self_dataframe_from_data()
