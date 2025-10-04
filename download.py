#!/usr/bin/env python3
"""
Download clang-format or clang-tidy wheel for the current platform.

This script automatically detects your platform and downloads the appropriate
wheel from the GitHub releases of cpp-linter/clang-tools-wheel.
"""

import argparse
import platform
import subprocess
import sys
import urllib.request
import json
from pathlib import Path


def get_platform_tag():
    """Detect the current platform and return the appropriate wheel tag."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Normalize machine architecture names
    arch_map = {
        "x86_64": "x86_64",
        "amd64": "x86_64",
        "aarch64": "aarch64",
        "arm64": "arm64",
        "armv7l": "armv7l",
        "i386": "i686",
        "i686": "i686",
        "ppc64le": "ppc64le",
        "s390x": "s390x",
    }

    arch = arch_map.get(machine, machine)

    if system == "darwin":  # macOS
        if arch in ["arm64", "aarch64"]:
            return ["macosx_11_0_arm64"]
        else:
            return ["macosx_10_9_x86_64"]

    elif system == "linux":
        # Try to detect libc type
        try:
            # Check if we're on musl
            result = subprocess.run(
                ["ldd", "--version"], capture_output=True, text=True, check=False
            )
            if "musl" in result.stderr.lower():
                libc = "musllinux"
            else:
                libc = "manylinux"
        except (FileNotFoundError, subprocess.SubprocessError):
            # Default to manylinux if ldd is not available
            libc = "manylinux"

        if libc == "manylinux":
            if arch == "x86_64":
                # Try multiple manylinux versions in order of preference
                return [
                    "manylinux_2_27_x86_64.manylinux_2_28_x86_64",
                    "manylinux_2_17_x86_64.manylinux2014_x86_64",
                ]
            elif arch == "aarch64":
                return [
                    "manylinux_2_26_aarch64.manylinux_2_28_aarch64",
                    "manylinux_2_17_aarch64.manylinux2014_aarch64",
                ]
            elif arch == "i686":
                return [
                    "manylinux_2_26_i686.manylinux_2_28_i686",
                    "manylinux_2_17_i686.manylinux2014_i686",
                ]
            elif arch == "ppc64le":
                return ["manylinux_2_26_ppc64le.manylinux_2_28_ppc64le"]
            elif arch == "s390x":
                return ["manylinux_2_26_s390x.manylinux_2_28_s390x"]
            elif arch == "armv7l":
                return ["manylinux_2_31_armv7l"]
        else:  # musllinux
            return [f"musllinux_1_2_{arch}"]

    elif system == "windows":
        if arch == "amd64" or arch == "x86_64":
            return ["win_amd64"]
        elif arch == "arm64":
            return ["win_arm64"]
        else:
            return ["win32"]

    raise ValueError(f"Unsupported platform: {system} {machine}")


def get_release_info(repo="cpp-linter/clang-tools-wheel", version=None):
    """Get information about a specific release or latest release from GitHub API."""
    if version:
        # Remove 'v' prefix if present for the API call
        clean_version = version.lstrip("v")
        url = f"https://api.github.com/repos/{repo}/releases/tags/v{clean_version}"
    else:
        url = f"https://api.github.com/repos/{repo}/releases/latest"

    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        if version:
            raise RuntimeError(
                f"Failed to fetch release info for version {version}: {e}"
            )
        else:
            raise RuntimeError(f"Failed to fetch latest release info: {e}")


def get_latest_release_info(repo="cpp-linter/clang-tools-wheel"):
    """Get information about the latest release from GitHub API."""
    return get_release_info(repo)


def find_wheel_asset(assets, tool, platform_tags, version=None):
    """Find the appropriate wheel asset for the given tool and platform."""
    # Try both naming conventions: clang-format and clang_format
    tool_underscore = tool.replace("-", "_")

    wheel_pattern_hyphen = f"{tool}-"
    wheel_pattern_underscore = f"{tool_underscore}-"

    if version:
        wheel_pattern_hyphen += f"{version}-"
        wheel_pattern_underscore += f"{version}-"

    wheel_pattern_hyphen += "py2.py3-none-"
    wheel_pattern_underscore += "py2.py3-none-"

    # Try each platform tag
    for platform_tag in platform_tags:
        for asset in assets:
            name = asset["name"]
            if (
                (
                    name.startswith(wheel_pattern_hyphen)
                    or name.startswith(wheel_pattern_underscore)
                )
                and name.endswith(".whl")
                and platform_tag in name
            ):
                return asset

    return None


def download_file(url, filename):
    """Download a file from URL to the specified filename."""
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Successfully downloaded {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download clang-format or clang-tidy wheel for current platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s clang-format                    # Download latest clang-format
  %(prog)s clang-tidy                      # Download latest clang-tidy
  %(prog)s clang-format --version 20.1.8  # Download specific version
  %(prog)s clang-format --output ./wheels # Download to specific directory
        """,
    )

    parser.add_argument(
        "tool",
        choices=["clang-format", "clang-tidy"],
        help="Tool to download (clang-format or clang-tidy)",
    )
    parser.add_argument(
        "--version", "-v", help="Specific version to download (default: latest)"
    )
    parser.add_argument(
        "--output",
        "-o",
        default=".",
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "--platform", help="Override platform detection (advanced usage)"
    )
    parser.add_argument(
        "--list-platforms",
        action="store_true",
        help="List all available platforms for the latest release",
    )

    args = parser.parse_args()

    try:
        # Get release information
        if args.version:
            print(f"Fetching release information for version {args.version}...")
        else:
            print("Fetching latest release information...")

        release_info = get_release_info(version=args.version)

        if args.list_platforms:
            print(
                f"Available platforms for {args.tool} in release {release_info['tag_name']}:"
            )
            # Try both naming conventions: clang-format and clang_format
            tool_underscore = args.tool.replace("-", "_")
            tool_assets = [
                a
                for a in release_info["assets"]
                if (
                    (
                        a["name"].startswith(f"{args.tool}-")
                        or a["name"].startswith(f"{tool_underscore}-")
                    )
                    and a["name"].endswith(".whl")
                )
            ]
            platforms = set()
            for asset in tool_assets:
                name = asset["name"]
                # Extract platform part after py2.py3-none-
                # First remove .whl extension, then split by '-'
                name_without_ext = name.replace(".whl", "")
                parts = name_without_ext.split("-")
                if len(parts) >= 5:
                    # Platform part starts after 'py2.py3-none'
                    platform_part = "-".join(parts[4:])
                    platforms.add(platform_part)

            for platform_tag in sorted(platforms):
                print(f"  {platform_tag}")
            return

        # Detect platform
        if args.platform:
            platform_tags = [args.platform]
        else:
            try:
                platform_tags = get_platform_tag()
                print(f"Detected platform: {platform_tags[0]}")
            except ValueError as e:
                print(f"Error: {e}")
                print(
                    "Use --platform to specify manually, or --list-platforms to see available options"
                )
                return 1

        # Find the wheel
        # Extract version from release tag for pattern matching
        release_version = release_info["tag_name"].lstrip("v")
        wheel_asset = find_wheel_asset(
            release_info["assets"], args.tool, platform_tags, release_version
        )

        if not wheel_asset:
            print(f"No wheel found for {args.tool} on platform {platform_tags[0]}")
            if args.version:
                print(f"Requested version: {args.version}")
            print(f"Available release: {release_info['tag_name']}")
            print("Use --list-platforms to see all available platforms")
            return 1

        # Create output directory if it doesn't exist
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Download the wheel
        filename = output_dir / wheel_asset["name"]
        if download_file(wheel_asset["browser_download_url"], filename):
            print("\nWheel downloaded successfully!")
            print(f"File: {filename}")
            print(f"Size: {wheel_asset['size'] / (1024 * 1024):.1f} MB")
            print(f"\nTo install: pip install {filename}")
        else:
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
