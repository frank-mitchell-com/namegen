`namegen.py` generates a list of random words based on a simple grammar.
It can be used to generate names for science-fiction aliens or words in
a constructed language.

### Usage

```
usage: namegen.py [-h] [-n NUMBER] [-o OUTPUT] namefile

Generate a list of names based on a grammar

positional arguments:
  namefile              JSON file specifying random name generator

options:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        number of names to generate
  -o OUTPUT, --output OUTPUT
                        output file
```

### Random Name Generator Grammar Format

The grammars for `namegen.py` constructs a name as a sequence of *syllables*.
Each grammar specification is a single JSON Object with the following keys:

`min_syllables`:
: The minimum number of syllables in a name.

`max_syllables`:
: The maximum number of syllables in a name.

`initial`:
: A List of Strings containing zero or more letters, ideally consonants.

`vowels`
: A List of Strings containing zero or more letters, ideally vowels.

`medial` (optional):
: A List of Strings containing zero or more letters that occur *between*
  `vowels`.  If not given, the code will use the product of
  `initial` &times; `final`.

`final` (optional):
: A List of Strings containing zero or more letters that occur at the end
  of a name (or a syllable, if `medial` is not given). If `final` is not
  given, it is assumed to be equal to `[""]` (a List of the empty string).

See the `grammar/*-grammar.json` files in this directory.
