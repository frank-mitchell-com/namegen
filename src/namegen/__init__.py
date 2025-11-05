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

import bisect
import random
from collections.abc import Mapping
from typing import Protocol

# maximum retries to find a unique name
MAX_RETRIES: int = 1_000_000


class NameSource(Protocol):
    """
    Compatibility with methods on `namemaker.make_name_set` result.
    """

    def make_name(self) -> str: ...

    def add_to_history(self, name: str) -> None: ...


class WeightedChoiceTable(Mapping):
    def __init__(self, obj: list[str] | dict[str, float]):
        self._map: dict[str, float] | None = None
        self._choices: list[str] = []
        self._weights: list[float] = []

        if isinstance(obj, dict):
            mp: dict = obj
            for key in iter(mp):
                self.set_weight_for_choice(str(key), float(mp[key]))
        elif isinstance(obj, list):
            lst: list = obj
            for key in iter(lst):
                self.set_weight_for_choice(str(key), 1)
        else:
            raise TypeError

    def set_weight_for_choice(self, choice: str, weight: float) -> None:
        i: int = bisect.bisect(self._choices, choice)
        if i < len(self._choices) and self._choices[i] == choice:
            self._weights[i] = weight
        else:
            self._choices.insert(i, choice)
            self._weights.insert(i, weight)
        self._map = None

    def choose(self) -> str:
        return random.choices(self._choices, self._weights)[0]

    @property
    def mapview(self):
        if self._map is None:
            self._map = dict(zip(self._choices, self._weights))
        return self._map

    def __contains__(self, item):
        return item in self.mapview

    def __getitem__(self, key):
        return self.mapview[key]

    def __iter__(self):
        return iter(self.mapview)

    def __len__(self):
        return len(self.mapview)

    def __str__(self) -> str:
        buffer: list[str] = ["{"]
        for i in range(len(self._choices)):
            if i > 0:
                buffer.append(", ")
            buffer.append(f"{self._choices[i]}:={self._weights[i]}")
        buffer.append("}")
        return "".join(buffer)


class NameGenerator:
    def __init__(self, config: dict, no_caps: bool = False) -> str:
        assert "min_syllables" in config
        assert "max_syllables" in config
        assert "initial" in config
        assert "vowels" in config

        self._pastnames: set[str] = set()
        self._no_caps = no_caps

        self._max: int
        self._min: int
        self._initial: WeightedChoiceTable
        self._medial: WeightedChoiceTable | None
        self._final: WeightedChoiceTable | None
        self._vowels: WeightedChoiceTable

        # TODO: Verify types from `config`
        self._min = int(config["min_syllables"])
        self._max = int(config["max_syllables"])
        self._vowels = WeightedChoiceTable(config["vowels"])
        self._initial = WeightedChoiceTable(config["initial"])
        if "final" not in config or not config["final"]:
            self._final = None
        else:
            self._final = WeightedChoiceTable(config["final"])
        if "medial" not in config or not config["medial"]:
            self._medial = None
        else:
            self._medial = WeightedChoiceTable(config["medial"])

    def _raw_name(self) -> str:
        nsyllables: int = random.randint(self._min, self._max)

        name_seq: list[str] = [
            self._initial.choose(),
            self._vowels.choose(),
        ]
        for _ in range(1, nsyllables):
            if self._medial:
                name_seq.append(self._medial.choose())
            else:
                if self._final:
                    name_seq.append(self._final.choose())
                name_seq.append(self._initial.choose())
            name_seq.append(self._vowels.choose())
        if self._final:
            name_seq.append(self._final.choose())

        result: str = "".join(name_seq)
        if not self._no_caps:
            result = result.capitalize()
        return result

    def make_name(self) -> str:
        count: int = 0
        newname: str = self._raw_name()
        while newname and newname in self._pastnames and count < MAX_RETRIES:
            newname = self._raw_name()
            count += 1
        self._pastnames.add(newname)
        return newname

    def add_to_history(self, name: str) -> None:
        self.pastnames.add(name)
