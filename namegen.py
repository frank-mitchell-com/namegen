#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = []
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
import itertools
import json
import random
from collections.abc import Sequence
from typing import Protocol

DEFAULT_NUMBER_OF_NAMES = 100

# maximum retries to find a unique star name
MAX_RETRIES: int = 1_000_000


class NameSource(Protocol):
    def name(self) -> str: ...


class SimpleNameSource:
    def __init__(self, jsonsrc: dict):
        assert "min_syllables" in jsonsrc
        assert "max_syllables" in jsonsrc
        assert "initial" in jsonsrc
        assert "vowels" in jsonsrc

        self._max: int
        self._min: int
        self._initial: Sequence[str]
        self._medial: Sequence[str]
        self._final: Sequence[str]
        self._vowels: Sequence[str]

        # TODO: Verify types from `jsonsrc`
        self._min = jsonsrc["min_syllables"]
        self._max = jsonsrc["max_syllables"]
        self._vowels = jsonsrc["vowels"]
        self._initial = jsonsrc["initial"]
        if "final" not in jsonsrc or not jsonsrc["final"]:
            self._final = [""]
        else:
            self._final = jsonsrc["final"]
        if "medial" not in jsonsrc or not jsonsrc["medial"]:
            self._medial = [
                "".join(x) for x in itertools.product(self._final, self._initial)
            ]
        else:
            self._medial = jsonsrc["medial"]

    def name(self) -> str:
        nsyllables: int = random.randint(self._min, self._max)

        name_seq: list[str] = [
            random.choice(self._initial),
            random.choice(self._vowels),
        ]
        for _ in range(1, nsyllables):
            name_seq.extend((random.choice(self._medial), random.choice(self._vowels)))
        name_seq.append(random.choice(self._final))

        return "".join(name_seq).capitalize()


class NameUniquifier:
    def __init__(self, source: NameSource) -> None:
        self._source = source
        self._pastnames: set[str] = set()

    def name(self) -> str:
        count: int = 0
        newname: str = self._source.name()
        while newname and newname in self._pastnames and count < MAX_RETRIES:
            newname = self._source.name()
            count += 1
        self._pastnames.add(newname)
        return newname


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
    args = parser.parse_args()

    namesrc: NameSource

    with args.namefile as jsonfile:
        namesrc = NameUniquifier(SimpleNameSource(json.load(jsonfile)))

    with args.output as outfile:
        for _ in range(args.number):
            outfile.write(f"{namesrc.name()}\n")


if __name__ == "__main__":
    main()
