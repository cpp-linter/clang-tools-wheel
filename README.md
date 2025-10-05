# clang-tools Python distribution

[![Build clang-tools wheels](https://github.com/cpp-linter/clang-tools-wheel/actions/workflows/clang-tools-release.yml/badge.svg)](https://github.com/cpp-linter/clang-tools-wheel/actions/workflows/clang-tools-release.yml)

This project provides **Python wheels** for clang-tools like `clang-format`, `clang-tidy`, making them easy to install via **pip**.

## Quick Install

You can download and install `clang-format` or `clang-tidy` wheels using the following command:

```bash
# Download latest clang-format wheel
curl -LsSf https://cpp-linter.github.io/install-wheel.sh | bash -s -- clang-format

# Download clang-tidy with specific version
curl -LsSf https://cpp-linter.github.io/install-wheel.sh | bash -s -- clang-tidy --version 21.1.2

# List available platforms
curl -LsSf https://cpp-linter.github.io/install-wheel.sh | bash -s -- --list clang-format

# Download to specific directory
curl -LsSf https://cpp-linter.github.io/install-wheel.sh | bash -s -- clang-format --output ./wheels
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

## Supported Platforms

| Platform | Architecture | Wheel Tag |
|----------|-------------|-----------|
| **macOS** | Intel (x86_64) | `macosx_10_9_x86_64` |
| **macOS** | Apple Silicon (arm64) | `macosx_11_0_arm64` |
| **Linux** | x86_64 (glibc) | `manylinux_2_27_x86_64` |
| **Linux** | x86_64 (musl) | `musllinux_1_2_x86_64` |
| **Linux** | aarch64 (glibc) | `manylinux_2_26_aarch64` |
| **Linux** | aarch64 (musl) | `musllinux_1_2_aarch64` |
| **Linux** | i686 (glibc) | `manylinux_2_26_i686` |
| **Linux** | i686 (musl) | `musllinux_1_2_i686` |
| **Linux** | ppc64le (glibc) | `manylinux_2_26_ppc64le` |
| **Linux** | ppc64le (musl) | `musllinux_1_2_ppc64le` |
| **Linux** | s390x (glibc) | `manylinux_2_26_s390x` |
| **Linux** | s390x (musl) | `musllinux_1_2_s390x` |
| **Linux** | armv7l (glibc) | `manylinux_2_31_armv7l` |
| **Linux** | armv7l (musl) | `musllinux_1_2_armv7l` |
| **Windows** | 64-bit | `win_amd64` |
| **Windows** | 32-bit | `win32` |
| **Windows** | ARM64 | `win_arm64` |

## Acknowledgements

This project builds on the excellent work of:

* [clang-format-wheel](https://github.com/ssciwr/clang-format-wheel)
* [clang-tidy-wheel](https://github.com/ssciwr/clang-tidy-wheel)

We redistribute these wheels through [GitHub releases](https://github.com/cpp-linter/clang-tools-wheel/releases) for the [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) project.
