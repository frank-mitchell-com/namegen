`namegen` generates a list of random words based on a simple grammar.
It can be used to generate names for science-fiction aliens or words in
a constructed language.

## Build

Install `uv` and type

`uv build`

TODO

## Usage

Here is a simple program that loads a grammar from an external file and
generates 10 unique names.

```py
import json
from namegen import NameGenerator, NameSource

FILENAME = "grammars/zeta-grammar.json"


def main() -> None:

    namesrc: NameSource

    with open(FILENAME, "r") as jsonfile:
        namesrc = NameGenerator(json.load(jsonfile))

    for _ in range(10):
        print(namesrc.make_name())


if __name__ == "__main__":
    main()
```

See `main.py` in the full source distribution for a full-featured driver
program.

See the `grammar/*-grammar.json` files in the full source distribution
for example grammars.


## Random Name Generator Grammar Format

`NameGenerator` constructs a name as a sequence of *syllables*.
Each grammar configuration is a single Python `dict` ith the following keys:

`min_syllables`:
: The minimum number of syllables in a name ('int').

`max_syllables`:
: The maximum number of syllables in a name ('int').

`initial`:
: A Letter Table containing zero or more letters, ideally consonants
  or the empty string.

`vowels`:
: A Letter Table containing zero or more letters, ideally vowels.

`medial` (optional):
: A Letter Table containing zero or more letters (consonant clusters) that
  occur *between* vowels`.  If not given, the code will use the product of
  initial` &times; `final`.

`final` (optional):
: A Letter Table containing zero or more letters that occur at
  the end of a name (or a syllable, if `medial` is not given). If `final` is
  not given, it is assumed to be equal to a Letter Table containing only
  the empty string ("").

A "Letter Table" is either a Python `list` of strings used to construct a Name,
or a Python 'dict` whose keys are Python strings and whose values are Python
`int`s or `float`s. The `dict` form attaches statistical weights for the
corresponding "letters", while the `list` form denotes a flat distribution.
