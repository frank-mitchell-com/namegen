`namegen.py` generates a list of random words based on a simple grammar.
It can be used to generate names for science-fiction aliens or words in
a constructed language.

### Usage

This project provides a simple driver program:

```
usage: main.py [-h] [-n NUMBER] [-o OUTPUT] [-C] namefile

Generate a list of names based on a grammar

positional arguments:
  namefile             JSON file specifying random name generator

options:
  -h, --help           show this help message and exit
  -n, --number NUMBER  number of names to generate
  -o, --output OUTPUT  output file
  -C, --no-caps        preserve capitalization in the initial symbols
```

### Random Name Generator Grammar Format

The grammars for `namegen.py` constructs a name as a sequence of *syllables*.
Each grammar specification is a single Python `dict` ith the following keys:

`min_syllables`:
: The minimum number of syllables in a name.

`max_syllables`:
: The maximum number of syllables in a name.

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

See the `grammar/*-grammar.json` files in this directory for examples.
