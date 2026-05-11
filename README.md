# RQMC for High-Dimensional Integration in ML  
## RQMC для высокоразмерного интегрирования в машинном обучении

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://www.python.org/)
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Docker|pytest|CI-green)]()
[![Status](https://img.shields.io/badge/Status-Research_Playbook-orange)]()

A structured, reproducible research playbook on Randomized Quasi-Monte Carlo (RQMC) methods for high-dimensional integration in machine learning. Focus: effective dimensionality, compute-aware benchmarking, and variance reduction in probabilistic pipelines.

Структурированное исследовательское руководство по рандомизированным методам квази-Монте-Карло (RQMC) для высокоразмерного интегрирования в ML. Фокус: эффективная размерность, учёт вычислительного бюджета и снижение дисперсии в вероятностных пайплайнах.

---

## Project Structure
```
rqmc-ml-playbook/
├── src/          # Production-grade modules (generators, metrics, experiments)
├── tests/        # Unit & integration tests (pytest, coverage ≥80%)
├── configs/      # YAML/TOML experiment configs, seeds, hyperparameters
├── notebooks/    # Prototyping, visualization, interactive demos
├── theory/       # LaTeX manuscript, bibliography, figures
├── docs/         # Technical docs, decision logs, reproduction guides
├── scripts/      # CLI runners for benchmarks, PDF builds, validation
├── data/         # Generated artifacts (git-ignored, documented)
├── .github/      # Issue/PR templates, CI/CD workflows
├── pyproject.toml# Modern packaging & dependency management (PEP 621)
├── Dockerfile    # Reproducible environment, pinned base image
├── Makefile      # Targeted commands: setup, test, pdf, benchmark, clean
├── README.md     # This file
└── CITATION.cff  # Machine-readable citation metadata
```

## Quick Start
```bash
# 1. Clone & enter
git clone https://github.com/fimaruyn/rqmc-ml-playbook.git
cd rqmc-ml-playbook

# 2. Reproduce environment (Phase 2)
make setup

# 3. Run baseline discrepancy benchmark (Phase 3)
make benchmark-discrepancy

# 4. Build theory manuscript (Phase 4)
make pdf
```

## Documentation
- [Contribution Guidelines](CONTRIBUTING.md)
- [Decision Log](docs/decisions.log)
- [Reproducibility Protocol](docs/reproduction.md)

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Citation
If you use this work, please cite via `CITATION.cff` or GitHub's "Cite this repository" feature.
