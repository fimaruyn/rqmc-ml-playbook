#!/usr/bin/env python
"""Verify that the research environment is correctly set up."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Final

import psutil  # type: ignore[import-untyped]


def check_python_version() -> bool:
    """Check that Python version is >= 3.12."""
    required: Final[tuple[int, int]] = (3, 12)
    current = sys.version_info[:2]
    if current < required:
        print(f"❌ Python {required[0]}.{required[1]}+ required, got {current[0]}.{current[1]}")
        return False
    print(f"✅ Python {current[0]}.{current[1]}")
    return True


def check_package_installed(package_name: str, import_name: str | None = None) -> bool:
    """Check that a package is installed and importable.

    Args:
        package_name: Name as listed in pyproject.toml / PyPI
        import_name: Name used in `import` statement (defaults to package_name)
    """
    import_name = import_name or package_name
    try:
        __import__(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name}: {e}")
        return False

def check_disk_space(min_gb: float = 5.0) -> bool:
    """Check that sufficient disk space is available."""
    usage = psutil.disk_usage(str(Path.cwd()))
    available_gb = usage.free / (1024**3)
    if available_gb < min_gb:
        print(f"❌ Disk space: {available_gb:.1f} GB available, {min_gb} GB required")
        return False
    print(f"✅ Disk space: {available_gb:.1f} GB")
    return True


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'='*60}\n{title}\n{'='*60}")


def main() -> None:
    """Run all verification checks."""
    print_header("Environment Verification")

    checks = [
        ("Python version", check_python_version),
        ("Package: numpy", lambda: check_package_installed("numpy")),
        ("Package: scipy", lambda: check_package_installed("scipy")),
        ("Package: salib", lambda: check_package_installed("salib", import_name="SALib")),
        ("Disk space", check_disk_space),
    ]

    results = [check() for _, check in checks]

    print_header("Summary")
    passed = sum(results)
    total = len(results)
    print(f"{passed}/{total} checks passed")

    if passed == total:
        print("🎉 Environment is ready for research!")
        sys.exit(0)
    else:
        print("⚠️  Some checks failed. Review above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
