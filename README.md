# clang-tools-wheel

[![release](https://img.shields.io/github/v/release/cpp-linter/clang-tools-wheel?label=release&labelColor=454a63&color=007ec6)](https://github.com/cpp-linter/clang-tools-wheel/releases)
[![part of cpp-linter](https://img.shields.io/badge/part%20of-cpp--linter-ffc20a?labelColor=454a63)](https://cpp-linter.github.io/)

Python wheels of `clang-format` and `clang-tidy`, built from the [ssciwr](https://github.com/ssciwr) projects and published as GitHub releases.

[Website](https://cpp-linter.github.io/) ·
[Get started](https://cpp-linter.github.io/getting-started/#just-the-clang-tools) ·
[Discussions](https://github.com/orgs/cpp-linter/discussions)

## Quick start

The helper script downloads the wheel for your platform; pip then installs it:

```bash
# Download latest clang-format wheel
curl -LsSf https://cpp-linter.github.io/install-wheel.sh | bash -s -- clang-format
pip install ./clang_format-*.whl
```

## Usage

```bash
# Download clang-tidy with specific version
curl -LsSf https://cpp-linter.github.io/install-wheel.sh | bash -s -- clang-tidy --version 22.1.3

# List available platforms
curl -LsSf https://cpp-linter.github.io/install-wheel.sh | bash -s -- --list clang-format

# Download to specific directory
curl -LsSf https://cpp-linter.github.io/install-wheel.sh | bash -s -- clang-format --output ./wheels
```

`--version` takes a release version such as `22.1.3` from the [releases](https://github.com/cpp-linter/clang-tools-wheel/releases), not an LLVM major version such as `21`.

## PyPI packages

`pip install clang-format` and `pip install clang-tidy` install ssciwr's own builds from PyPI, not
the wheels from these releases. [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks)
installs those PyPI packages too.

## Supported platforms

The table lists the `clang-format` wheels. `clang-tidy` wheels exist only for macOS, Linux x86_64 and i686 (glibc and musl), Linux aarch64 (glibc) and Windows 64-bit and 32-bit, and some of their Linux tags differ; `--list clang-tidy` prints them.

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

The wheels are built from [clang-format-wheel](https://github.com/ssciwr/clang-format-wheel) and [clang-tidy-wheel](https://github.com/ssciwr/clang-tidy-wheel) by ssciwr, included here as git submodules.

## Contributing

See [CONTRIBUTING.md](https://github.com/cpp-linter/clang-tools-wheel/blob/main/CONTRIBUTING.md). Issues are turned off in this repository, so report problems in [Discussions](https://github.com/orgs/cpp-linter/discussions) or open a [pull request](https://github.com/cpp-linter/clang-tools-wheel/pulls).

## License

The build scripts and workflows in this repository are released under the
[Apache License 2.0](https://github.com/cpp-linter/clang-tools-wheel/blob/main/LICENSE). The wheels
also carry ssciwr's license files, and the clang-format and clang-tidy binaries inside them are
under the [Apache License v2.0 with LLVM Exceptions](https://llvm.org/LICENSE.txt).
