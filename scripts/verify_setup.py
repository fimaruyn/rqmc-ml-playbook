#!/usr/bin/env python
"""
Verification script for Docker-based research environment.
Run via: make run ARGS="python scripts/verify_setup.py"
"""
import sys
import platform
import subprocess
from pathlib import Path


def check_python_version():
    """Verify Python version matches project requirements."""
    major, minor = sys.version_info[:2]
    assert major == 3 and minor == 12, f"Expected Python 3.12, got {major}.{minor}"
    print(f"✅ Python {major}.{minor}.{sys.version_info.micro}")


def check_core_dependencies():
    """Verify all core dependencies are importable."""
    deps = {
        "numpy": "1.24",
        "scipy": "1.12",
        "salib": "1.4",
        "loguru": "0.7",
        "yaml": "6.0",
        "pandas": "2.0",
        "matplotlib": "3.7",
    }
    
    for module, min_version in deps.items():
        try:
            mod = __import__(module)
            version = getattr(mod, "__version__", "unknown")
            print(f"✅ {module} {version}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    return True


def check_project_structure():
    """Verify expected project directories exist."""
    required_dirs = ["src", "tests", "configs", "theory", "docs", "scripts"]
    for dir_name in required_dirs:
        assert Path(dir_name).is_dir(), f"Missing directory: {dir_name}"
    print(f"✅ Project structure verified ({len(required_dirs)} directories)")


def check_git_repository():
    """Verify running inside a Git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Git repository: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Not running inside a Git repository (optional for development)")
        return False


def check_compute_environment():
    """Log compute environment for reproducibility."""
    print(f"🖥️  Platform: {platform.platform()}")
    print(f"🖥️  Machine: {platform.machine()}")
    print(f"🖥️  Processor: {platform.processor() or 'N/A'}")
    
    try:
        import psutil
        print(f"🖥️  CPU cores: {psutil.cpu_count(logical=True)}")
        print(f"🖥️  RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    except ImportError:
        pass


def main():
    """Run all verification checks."""
    print("🔍 Verifying research environment setup...\n")
    
    checks = [
        ("Python version", check_python_version),
        ("Core dependencies", check_core_dependencies),
        ("Project structure", check_project_structure),
        ("Git repository", check_git_repository),
        ("Compute environment", check_compute_environment),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        try:
            result = check_func()
            results.append((name, result is not False))
        except AssertionError as e:
            print(f"❌ {e}")
            results.append((name, False))
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            results.append((name, False))
    
    print(f"\n{'='*60}")
    print("📊 VERIFICATION SUMMARY")
    print(f"{'='*60}")
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Environment is ready for research!")
        return 0
    else:
        print("⚠️  Some checks failed. Review output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())