"""Smoke test: verification of core research dependencies."""


def test_numpy_scipy_available():
    """Core numerical libraries must be importable."""
    import numpy as np
    import scipy

    assert np.__version__ >= "1.24"
    assert scipy.__version__ >= "1.12"

def test_loguru_available():
    """Structured logging library must be available."""
    from loguru import logger

    assert logger is not None
