#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = [
# ]
# ///

# MIT License
#
# Copyright (c) 2025 Frank Mitchell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# n the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import json
from namegen import NameGenerator, NameSource


DEFAULT_NUMBER_OF_NAMES = 100


def main() -> None:
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Generate a list of names based on a grammar"
    )
    parser.add_argument(
        "namefile",
        help="JSON file specifying random name generator",
        type=argparse.FileType(mode="r", encoding="UTF-8"),
    )
    parser.add_argument(
        "-n",
        "--number",
        help="number of names to generate",
        default=DEFAULT_NUMBER_OF_NAMES,
        type=int,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file",
        default="-",
        type=argparse.FileType(mode="w", encoding="UTF-8"),
    )
    parser.add_argument(
        "-C",
        "--no-caps",
        help="preserve capitalization in the initial symbols",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()

    namesrc: NameSource

    with args.namefile as jsonfile:
        namesrc = NameGenerator(json.load(jsonfile), args.no_caps)

    with args.output as outfile:
        for _ in range(args.number):
            outfile.write(f"{namesrc.make_name()}\n")


if __name__ == "__main__":
    main()
