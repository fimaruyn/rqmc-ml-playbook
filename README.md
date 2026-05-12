# RQMC for High-Dimensional Integration in ML  
## RQMC для высокоразмерного интегрирования в машинном обучении

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB.svg)](https://www.python.org/)
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Docker|pytest|CI-green)]()
[![Status](https://img.shields.io/badge/Status-Research_Playbook-orange)]()

A structured, reproducible research playbook on Randomized Quasi-Monte Carlo (RQMC) methods for high-dimensional integration in machine learning. Focus: effective dimensionality, compute-aware benchmarking, and variance reduction in probabilistic pipelines.

Структурированное исследовательское руководство по рандомизированным методам квази-Монте-Карло (RQMC) для высокоразмерного интегрирования в машинном обучении. Фокус: эффективная размерность, учёт вычислительного бюджета и снижение дисперсии в вероятностных пайплайнах.

---

## Project Structure / Структура проекта

```
rqmc-ml-playbook/
├── src/                    # Production-grade Python modules
├── tests/                  # Unit & integration tests (pytest)
├── configs/                # YAML/TOML experiment configurations
├── notebooks/              # Prototyping & interactive exploration
├── theory/                 # LaTeX manuscript, bibliography, figures
├── docs/                   # Technical documentation, decision logs
├── scripts/                # CLI runners for benchmarks & automation
├── data/                   # Generated artifacts (git-ignored)
├── .github/                # Issue/PR templates, CI/CD workflows
├── pyproject.toml          # Modern packaging & dependency management
├── Dockerfile              # Reproducible container environment
├── Makefile                # Unified command interface
├── README.md               # This file
└── CITATION.cff            # Machine-readable citation metadata
```

## Quick Start / Быстрый старт

```bash
# 1. Clone the repository
git clone https://github.com/[your-username]/rqmc-ml-playbook.git
cd rqmc-ml-playbook

# 2. Build the Docker environment (Stage 2)
make build

# 3. Verify setup
make run ARGS="python scripts/verify_setup.py"

# 4. Start interactive development
make shell
```

## Documentation / Документация

- [Contribution Guidelines](docs/CONTRIBUTING.md) — Coming soon
- [Decision Log](docs/decisions.log) — Coming soon
- [Reproducibility Protocol](docs/reproduction.md) — Coming soon

## License / Лицензия

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Данный проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## Citation / Цитирование

If you use this work, please cite via `CITATION.cff` or GitHub's "Cite this repository" feature.

При использовании данной работы просьба цитировать через файл `CITATION.cff` или функцию GitHub "Cite this repository".