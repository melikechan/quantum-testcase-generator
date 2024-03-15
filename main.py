import os
import sys
import argparse


def init_parser():
    parser = argparse.ArgumentParser("Generate testcases.")

    # Add arguments

    # Required arguments
    parser.add_argument("-n", help="number of testcases", type=int)
    parser.add_argument(
        "--format-json", help="format of input (JSON)", type=str)
    parser.add_argument("--solution", help="solution file", type=str)

    # Optional arguments
    parser.add_argument("--input", help="input file prefix", type=str)
    parser.add_argument("--output", help="output file prefix", type=str)

    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")
    return parser


if __name__ == "__main__":
    init_parser()
