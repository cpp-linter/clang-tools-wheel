# clang-tools Python distribution

This project provides **Python wheels** for clang-tools including `clang-format`, `clang-tidy`, making them easy to install via pip.

We aim to publish wheels for each major and minor release of `clang-format` and `clang-tidy`.

## Use with pipx or uv

You can install clang-format or clang-tidy via [`pipx`](https://pypa.github.io/pipx/) or [`uv`](https://docs.astral.sh/uv/):

```bash
pipx install git+https://github.com/cpp-linter/clang-tools-wheel.git#subdirectory=clang-format
pipx install git+https://github.com/cpp-linter/clang-tools-wheel.git#subdirectory=clang-tidy
```

## Use from pre-commit

[pre-commit](https://pre-commit.com/) hooks are available for both `clang-format` and `clang-tidy`.

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/cpp-linter/cpp-linter-hooks
    rev: v1.1.3
    hooks:
      - id: clang-format
        args: [--style=file]  # Loads style from .clang-format file
      - id: clang-tidy
        args: [--checks=.clang-tidy] # Loads checks from .clang-tidy file
```

## Acknowledgements

This project builds on the excellent work of:

* [clang-format-wheel](https://github.com/ssciwr/clang-format-wheel)
* [clang-tidy-wheel](https://github.com/ssciwr/clang-tidy-wheel)

We redistribute these wheels through GitHub releases for the [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) project.
