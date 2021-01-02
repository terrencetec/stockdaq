"""
"""
import stockdaq.helloworld
import stockdaq.clitools


def test_helloworld():
    string = stockdaq.helloworld.helloworlds(1)
    assert string == 'Hello World!'
