"""Tests for stockdaq.utils.config
"""
import stockdaq.utils.config


def test_str2list():
    string = "Alpha Vantage, yfinance, quantdl  , abc"
    test_list = stockdaq.utils.config.str2list(string)
    correct_list = ["Alpha Vantage", "yfinance", "quantdl", "abc"]
    assert all([i==j for i, j in zip(test_list, correct_list)])
