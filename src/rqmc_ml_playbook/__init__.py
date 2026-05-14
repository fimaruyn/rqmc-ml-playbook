"""
RQMC-ML Playbook: Reproducible research environment for quasi-Monte Carlo methods in ML.

This package provides:
- RQMC sequence generators (Sobol, Halton) with Owen scrambling
- Effective dimensionality diagnostics (ANOVA-based)
- Compute-aware benchmarking utilities
- Integration with probabilistic ML pipelines (VI, gradient estimation)

All modules are designed for reproducibility, type safety, and Docker-based execution.
"""

__version__ = "0.1.0"
__author__ = "Vladimir Belov"
__email__ = "vladimir.belov.an@gmail.com"
__all__ = ["__author__", "__email__", "__version__"]
