"""Data manager
"""
import pandas as pd

import stockdaq.data.data


def segmenter(dataframe, criterion="date"):
    """Split dataframe into multiple stockdaq.data.data.Data objects

    Parameters
    ----------
    dataframe: pandas.core.frame.DataFrame
        Dataframe
    criterion: str
        "date", "month", or "year"

    Returns
    -------
    data_dict: dict of stockdaq.data.data.Data
        {"date", "month", or "year": stockdaq.data.data.Data} pair
        For example {"2020-01-01": ..., "2020-01-02": ..., ...}.
    """
    dates = []  # Not technically date, just the string version\
        # of the datetime column.
    slice_indexes = []
    data_dict = {}
    if criterion == "date":
        for i in range(len(dataframe.index)):
            date = str(dataframe.index[i].date())
            if date not in dates:
                dates.append(date)
                slice_indexes.append(i)
        slice_indexes.append(len(dataframe.index))

        for i in range(len(dates)):
            begin = slice_indexes[i]
            end = slice_indexes[i+1]
            datetime_column = dataframe.index[begin:end]
            open_ = dataframe.open.values[begin:end]
            high = dataframe.high.values[begin:end]
            low = dataframe.low.values[begin:end]
            close = dataframe.close.values[begin:end]
            volume = dataframe.volume.values[begin:end]
            data = stockdaq.data.data.Data(
                datetime_column=datetime_column,
                open_=open_,
                high=high,
                low=low,
                close=close,
                volume=volume,
            )
            data_dict[dates[i]] = data
    elif criterion == "month":
        raise ValueError("Month criterion not avaiable yet.")
    elif criterion == "year":
        raise ValueError("Year criterion not avaiable yet.")
    else:
        raise ValueError("Criterion not avaiable.")

    return data_dict


def extended_trading_splitter(dataframe, begin="9:30", end="15:59"):
    """Divide data into three segments: premkt, open, aftermkt.

    Parameters
    ----------
    dataframe: pandas.core.frame.DataFrame

    """
