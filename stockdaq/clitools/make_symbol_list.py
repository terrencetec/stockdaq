import argparse


def parser():
    parser = argparse.ArgumentParser(description="Make stock symbol list")
    parser.add_argument(
        "-i", "--input", type=str, help="Path of the companylist.csv file",
        required=True
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Path of the output symbol list file",
        required=True
    )
    parser.add_argument(
        "-O", "--overwrite", help="Overwrite if output file exists",
        action="store_true"
    )
    parser.add_argument(
        "-x", "--omit", type=str,
        help="Omit symbols with specified characters",
        nargs="*", default=["^", "."]
    )
    parser.add_argument(
        "-n", "--no-header", help="First row of the input is not header",
        action="store_true"
    )
    parser.add_argument(
        "-s", "--symbol-index", type=int, help="The column index of the stock"\
        " symbols", default=0
    )
    return parser


def main(args=None):
    import stockdaq

    options = parser().parse_args(args)
    input_path = options.input
    output_path = options.output
    overwrite = options.overwrite
    omit = options.omit
    has_header = not options.no_header
    symbol_index = options.symbol_index
    stockdaq.symbol.make_symbol_list(
        input_path,
        output_path,
        overwrite,
        omit,
        has_header,
        symbol_index
    )
