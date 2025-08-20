import pytest
import re
from namegen import NameGenerator, NameSource

@pytest.fixture
def grammar_cv():
    return { 
        "min_syllables": 1,
        "max_syllables": 5,
        "initial": ["b","c","d","f","g","h"],
        "vowels": ["a", "e", "i", "o", "u", "y"],
    }


@pytest.fixture
def grammar_cvc():
    return { 
        "min_syllables": 1,
        "max_syllables": 5,
        "initial": ["b","c","d","f","g","h"],
        "vowels": ["a", "e", "i", "o", "u", "y"],
        "final": ["j","k","l","m","n","p"],
    }


@pytest.fixture
def grammar_cvc2():
    return { 
        "min_syllables": 1,
        "max_syllables": 5,
        "initial": ["b","c","d","f","g","h"],
        "vowels": ["a", "e", "i", "o", "u", "y"],
        "medial": ["j","k","l","m","n","p"],
        "final": ["q","r","s","t","v","w"],
    }


def test_initial_vowel(grammar_cv):
    namesrc: NameSource = NameGenerator(grammar_cv, True)

    name: str = namesrc.make_name()

    pat = re.compile('^([bcdfgh][aeiouy]){1,5}$')

    assert pat.match(name) is not None, f"{name} does not match {pat}"


def test_initial_vowel_final(grammar_cvc):
    namesrc: NameSource = NameGenerator(grammar_cvc, True)

    name: str = namesrc.make_name()

    pat = re.compile('^([bcdfgh][aeiouy][jklmnp]){1,5}$')

    assert pat.match(name) is not None, f"{name} does not match {pat}"


def test_initial_vowel_medial_final(grammar_cvc2):
    namesrc: NameSource = NameGenerator(grammar_cvc2, True)

    name: str = namesrc.make_name()

    pat = re.compile('^[bcdfgh][aeiouy]([jklmnp][aeiouy]){0,4}[qrstvw]$')

    assert pat.match(name) is not None, f"{name} does not match {pat}"
