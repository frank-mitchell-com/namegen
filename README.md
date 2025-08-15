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
Each grammar specification is a single JSON Object with the following keys:

`min_syllables`:
: The minimum number of syllables in a name.

`max_syllables`:
: The maximum number of syllables in a name.

`initial`:
: A List or Object of Strings containing zero or more letters, ideally
  consonants. If an Object, the keys are letters, the values are numbers
  expressing weights for each letter or letter cluster.

`vowels`
: A List or Object of Strings containing zero or more letters, ideally vowels.
  If an Object, the keys are letters, the values are numbers expressing weights
  for each letter or letter cluster.

`medial` (optional):
: A List or Object of Strings containing zero or more letters that occur
  *between* vowels`.  If not given, the code will use the product of
  initial` &times; `final`.
  See `initial` for the keys and values expected in an Object.

`final` (optional):
: A List or Object of Strings containing zero or more letters that occur at
  the end of a name (or a syllable, if `medial` is not given). If `final` is
  not given, it is assumed to be equal to `[""]` (a List of the empty string).
  See `initial` for the keys and values expected in an Object.

See the `grammar/*-grammar.json` files in this directory.
