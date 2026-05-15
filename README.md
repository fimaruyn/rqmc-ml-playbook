# RQMC for High-Dimensional Integration in ML
## RQMC для высокоразмерного интегрирования в машинном обучении

[![CI/CD Pipeline](https://github.com/fimaruyn/rqmc-ml-playbook/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/fimaruyn/rqmc-ml-playbook/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)

A reproducible research environment for Randomized Quasi-Monte Carlo methods in high-dimensional integration.

Воспроизводимая исследовательская среда для методов рандомизированного квази-Монте-Карло в задачах высокоразмерного интегрирования.

---

## Project Structure

```
rqmc-ml-playbook/
├── src/rqmc_ml_playbook/   # Core Python modules
├── tests/                   # Unit and integration tests
├── theory/                  # LaTeX manuscript (XeLaTeX + polyglossia)
├── scripts/                 # Utility and benchmark scripts
├── configs/                 # Experiment configurations
├── pyproject.toml           # Project metadata and dependencies
├── Dockerfile               # Reproducible container environment
├── Makefile                 # Command interface
├── README.md                # This file
├── LICENSE                  # MIT License
└── CITATION.cff             # Citation metadata
```

---

## Quick Start

### Local development

```bash
git clone https://github.com/fimaruyn/rqmc-ml-playbook.git
cd rqmc-ml-playbook

uv sync --extra dev
uv run python scripts/verify_setup.py
uv run pytest tests/ -v
```

### Docker environment

```bash
make build
make run ARGS="-c 'import salib, numpy, scipy; print(\"Imports OK\")'"
make test
make pdf
```

---

## Continuous Integration

This repository uses GitHub Actions to automatically validate changes on push and pull request. The workflow performs:

- Code linting with ruff
- Static type checking with mypy
- Unit testing with pytest
- Docker image build and verification
- LaTeX manuscript compilation with XeLaTeX

All checks must pass before changes can be merged into the main branch.

---

## Documentation

- Contribution guidelines: `docs/CONTRIBUTING.md`
- Reproducibility protocol: `docs/reproduction.md`
- LaTeX manuscript: `theory/main.tex`

---

## License

This project is licensed under the MIT License. See LICENSE for details.

Проект распространяется под лицензией MIT. Подробности в файле LICENSE.

---

## Citation

If you use this work in your research, please cite via CITATION.cff or GitHub's "Cite this repository" feature.

При использовании данной работы в исследованиях просьба цитировать через файл CITATION.cff или функцию GitHub "Cite this repository".

```bibtex
@software{belov_rqmc_ml_playbook_2026,
  author = {Belov, Vladimir},
  title = {RQMC for High-Dimensional Integration in ML},
  year = {2026},
  url = {https://github.com/fimaruyn/rqmc-ml-playbook},
  version = {0.1.0},
  license = {MIT}
}
```