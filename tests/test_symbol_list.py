"""
"""
import stockdaq


def test_symbol_list():
    input_path = "data/companylist.csv"
    output_path1 = "data/stock_list.txt"
    output_path2 = "data/test_stocklist.txt"
    stockdaq.make_symbol_list(
        input_path=input_path,
        output_path=output_path1,
        overwrite=True,
        omit=["^", "."],
        has_header=True,
        symbol_index=0
    )
    stockdaq.make_symbol_list(
        input_path=input_path,
        output_path=output_path2,
        overwrite=True,
        omit=[],
        has_header=True,
        symbol_index=0
    )
    stock_list1 = stockdaq.get_symbol_list(
        path=output_path1,
        omit=[],
    )
    stock_list2 = stockdaq.get_symbol_list(
        path=output_path2,
        omit=["^","."]
    )
    assert stock_list1 == stock_list2
