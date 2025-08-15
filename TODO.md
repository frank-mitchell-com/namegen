TODO
====

## Testing

- Bounded tests based on simple grammar and regexp,
  e.g. `([bcdfghjkl][aeiou][mnpqrstvwxyz])*`

- Write unit tests for word generation

  1. Monkeypatch random elements
  2. Refactor out random elements & test remainder

- Write unit tests for format validation

## Packaging

- Package as Python library with single "main" public function or object.

- Post library on PyPI

- Use library in `nomadsec` project.

## Robustness

- Check syntax of input file (JSON Schema?)

- Write stress tests

- Multithreaded performance / robustness?

