#!/usr/bin/env python3
"""
Использование:
    # Сгенерировать все графики
    python scripts/generate_all_figures.py --all

    # Сгенерировать графики для конкретной главы
    python scripts/generate_all_figures.py --chapter 2

    # Сгенерировать конкретный график
    python scripts/generate_all_figures.py --figure fig_discrepancy_comparison

    # Указать альтернативную директорию для сохранения
    python scripts/generate_all_figures.py --all --output-dir ./custom/figures
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from scipy.stats import qmc, norm, t


# Настройки matplotlib для академических публикаций
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "legend.fontsize": 9,
    "figure.titlesize": 14,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.format": "pdf",
    "text.usetex": False,  # Отключено для совместимости с кириллицей
})

# Пути по умолчанию
DEFAULT_OUTPUT_DIR = Path("theory/figures")

# Цветовая палитра
COLORS = {
    "mc": "gray",
    "qmc": "steelblue",
    "rqmc": "coral",
    "reference": "black",
    "good": "green",
    "bad": "red",
}


logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO) -> None:
    """Настройка логирования."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )


def ensure_directory(path: Path) -> Path:
    """Создать директорию, если она не существует."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_figure(fig: plt.Figure, filename: str, output_dir: Path) -> None:
    """Сохранить фигуру в указанную директорию."""
    filepath = output_dir / filename
    fig.savefig(filepath)
    plt.close(fig)
    logger.info(f"✓ Сохранён: {filepath}")



def plot_discrepancy_comparison(output_dir: Path) -> None:
    """
    Рисунок 2.1: Сравнение распределений с разной неравномерностью.
    Иллюстрирует геометрический фактор неравенства Коксмы–Хлавки.
    """
    logger.info("Генерация: fig_discrepancy_comparison.pdf")
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Левый график: плохое распределение (большая D_N^*)
    axes[0].set_xlim(0, 1)
    axes[0].set_ylim(0, 1)
    axes[0].set_aspect("equal")
    axes[0].set_title("(a) Плохое распределение точек\n$D_N^* \\approx 0.4$", fontsize=12)
    axes[0].set_xlabel("$x_1$")
    axes[0].set_ylabel("$x_2$")
    
    np.random.seed(42)
    bad_points = np.random.rand(50, 2) ** 3  # Кластеризация
    axes[0].scatter(
        bad_points[:, 0], bad_points[:, 1],
        c=COLORS["bad"], s=30, alpha=0.6,
        edgecolors="darkred", linewidth=0.5
    )
    axes[0].grid(True, alpha=0.3)
    
    # Правый график: хорошее распределение (Соболя)
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].set_aspect("equal")
    axes[1].set_title("(b) Хорошее распределение (Соболя)\n$D_N^* \\approx 0.02$", fontsize=12)
    axes[1].set_xlabel("$x_1$")
    axes[1].set_ylabel("$x_2$")
    
    sampler = qmc.Sobol(d=2, seed=42)
    good_points = sampler.random(50)
    axes[1].scatter(
        good_points[:, 0], good_points[:, 1],
        c=COLORS["qmc"], s=30, alpha=0.6,
        edgecolors="darkblue", linewidth=0.5
    )
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle("Влияние неравномерности $D_N^*$ на точность интегрирования", fontsize=14, y=1.02)
    plt.tight_layout()
    save_figure(fig, "fig_discrepancy_comparison.pdf", output_dir)


def plot_function_variation(output_dir: Path) -> None:
    """
    Рисунок 2.2: Функции с разной вариацией Харди–Краузе.
    Иллюстрирует аналитический фактор неравенства Коксмы–Хлавки.
    """
    logger.info("Генерация: fig_function_variation.pdf")
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    x = np.linspace(0, 1, 1000)
    
    # Гладкая функция (малая вариация)
    f_smooth = 0.5 + 0.3 * np.sin(2 * np.pi * x)
    axes[0].plot(x, f_smooth, "b-", linewidth=2,
                 label=r"$f(x) = 0.5 + 0.3\sin(2\pi x)$")
    axes[0].fill_between(x, 0, f_smooth, alpha=0.3, color="blue")
    axes[0].set_title("(a) Гладкая функция\n$V_{HK}(f) \\approx 1.9$", fontsize=12)
    axes[0].set_xlabel("$x$")
    axes[0].set_ylabel("$f(x)$")
    axes[0].set_ylim(0, 1.2)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc="upper right", fontsize=9)
    
    # Осциллирующая функция (большая вариация)
    k = 20
    f_osc = 0.5 + 0.3 * np.sin(2 * np.pi * k * x)
    axes[1].plot(x, f_osc, "r-", linewidth=1.5,
                 label=rf"$f(x) = 0.5 + 0.3\sin(2\pi \cdot {k} x)$")
    axes[1].fill_between(x, 0, f_osc, alpha=0.3, color="red")
    axes[1].set_title(f"(b) Осциллирующая функция\n$V_{{HK}}(f) \\approx 38$", fontsize=12)
    axes[1].set_xlabel("$x$")
    axes[1].set_ylabel("$f(x)$")
    axes[1].set_ylim(0, 1.2)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc="upper right", fontsize=9)
    
    plt.suptitle("Влияние вариации $V_{HK}(f)$ на сложность интегрирования", fontsize=14, y=1.02)
    plt.tight_layout()
    save_figure(fig, "fig_function_variation.pdf", output_dir)


def plot_centred_lattice(output_dir: Path, m: int = 6) -> None:
    """
    Рисунок 2.3: Центрированная регулярная решётка $\Gamma_m^c$.
    Иллюстрирует определение 2.6 и Теорему 2.8.
    """
    logger.info(f"Генерация: fig_centred_lattice.pdf (m={m})")
    
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Настройки осей
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Скрытие рамок
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Оси со стрелками
    ax.annotate("", xy=(1.05, 0), xytext=(-0.05, 0),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="black"))
    ax.annotate("", xy=(0, 1.05), xytext=(0, -0.05),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="black"))
    
    # Пунктирная сетка разбиения
    for i in range(1, m):
        ax.axhline(i / m, color="gray", linestyle=":", linewidth=0.8)
        ax.axvline(i / m, color="gray", linestyle=":", linewidth=0.8)
    
    # Точки решётки: x_{k,j} = (2k_j + 1) / (2m)
    k = np.arange(m)
    k1, k2 = np.meshgrid(k, k)
    x_pts = (2 * k1 + 1) / (2 * m)
    y_pts = (2 * k2 + 1) / (2 * m)
    ax.scatter(x_pts, y_pts, color="black", s=25, zorder=3)
    
    # Выделение одной ячейки
    cell_x, cell_y = 1 / m, 2 / m
    rect = Rectangle((cell_x, cell_y), 1 / m, 1 / m,
                     facecolor="gray", alpha=0.45, edgecolor="none", zorder=2)
    ax.add_patch(rect)
    
    ax.set_title(f"Центрированная решётка $\\Gamma_{{{m}}}^c$ в $[0, 1]^2$", fontsize=12, pad=10)
    plt.tight_layout()
    save_figure(fig, "fig_centred_lattice.pdf", output_dir)



def plot_elementary_intervals(output_dir: Path) -> None:
    """
    Рисунок 3.1: Свойство элементарных интервалов для (0, 3, 2)-сети.
    Иллюстрирует Определение 3.3.
    """
    logger.info("Генерация: fig_elementary_intervals.pdf")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # (0, 3, 2)-сеть в базе 2 (8 точек)
    points = np.array([
        [1/16, 1/16], [9/16, 5/16], [5/16, 11/16], [13/16, 3/16],
        [3/16, 13/16], [11/16, 9/16], [7/16, 7/16], [15/16, 15/16],
    ])
    
    ax.scatter(points[:, 0], points[:, 1], c="black", s=80, zorder=5,
               edgecolors="black", linewidth=1.5)
    
    # Сетка делений
    for i in range(1, 8):
        ax.axhline(i / 8, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
        ax.axvline(i / 8, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
    
    # Элементарный интервал 1: d1=1, d2=2
    rect1 = Rectangle((0.5, 0.5), 0.5, 0.25, fill=True,
                      edgecolor="red", facecolor="red", alpha=0.25, lw=2.5)
    ax.add_patch(rect1)
    ax.text(0.75, 0.625, "1 точка", ha="center", va="center",
            fontsize=11, fontweight="bold", color="darkred")
    
    # Элементарный интервал 2: d1=3, d2=0
    rect2 = Rectangle((0.25, 0.0), 0.125, 1.0, fill=True,
                      edgecolor="blue", facecolor="blue", alpha=0.25, lw=2.5)
    ax.add_patch(rect2)
    ax.text(0.3125, 0.5, "1 точка", ha="center", va="center",
            fontsize=11, fontweight="bold", color="darkblue", rotation=90)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_title("$(0, 3, 2)$-сеть в базе $b=2$ (элементарные интервалы)", fontsize=14, pad=15)
    ax.set_xlabel("$x_1$", fontsize=12)
    ax.set_ylabel("$x_2$", fontsize=12)
    
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    
    custom_lines = [
        Line2D([0], [0], color="red", lw=2.5),
        Line2D([0], [0], color="blue", lw=2.5)
    ]
    ax.legend(custom_lines,
              ["Интервал ($d_1=1, d_2=2$)", "Интервал ($d_1=3, d_2=0$)"],
              loc="upper left", framealpha=0.9)
    
    plt.tight_layout()
    save_figure(fig, "fig_elementary_intervals.pdf", output_dir)


def plot_quality_parameter_t(output_dir: Path) -> None:
    """
    Рисунок 3.2: Влияние параметра качества $t$ на распределение точек.
    Иллюстрирует Замечание 3.4.
    """
    logger.info("Генерация: fig_quality_parameter_t.pdf")
    
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    
    # Хорошая сеть (низкое t)
    sobol = qmc.Sobol(2, seed=0)
    pts_good = sobol.random(16)
    
    ax[0].scatter(pts_good[:, 0], pts_good[:, 1], c="black", s=40, zorder=3)
    ax[0].set_title("Хорошая сеть (Низкое $t$)\nРавномерное заполнение", fontsize=12)
    ax[0].set_xlim(0, 1)
    ax[0].set_ylim(0, 1)
    ax[0].grid(True, linestyle=":", alpha=0.6)
    for i in range(1, 4):
        ax[0].axhline(i / 4, color="gray", linestyle="-", lw=1, alpha=0.5)
        ax[0].axvline(i / 4, color="gray", linestyle="-", lw=1, alpha=0.5)
    
    # Плохая сеть (высокое t) — имитация кластеризации
    np.random.seed(42)
    centers = np.array([[0.2, 0.2], [0.8, 0.8], [0.2, 0.8], [0.8, 0.2]])
    pts_bad = []
    for c in centers:
        cluster = np.random.normal(c, 0.05, (4, 2))
        pts_bad.append(cluster)
    pts_bad = np.clip(np.vstack(pts_bad), 0, 1)
    
    ax[1].scatter(pts_bad[:, 0], pts_bad[:, 1], c="black", s=40, zorder=3)
    ax[1].set_title("Плохая сеть (Высокое $t$)\nКластеризация точек", fontsize=12)
    ax[1].set_xlim(0, 1)
    ax[1].set_ylim(0, 1)
    ax[1].grid(True, linestyle=":", alpha=0.6)
    for i in range(1, 4):
        ax[1].axhline(i / 4, color="red", linestyle="--", lw=1.5, alpha=0.7)
        ax[1].axvline(i / 4, color="red", linestyle="--", lw=1.5, alpha=0.7)
    
    for a in ax:
        a.set_aspect("equal")
        a.set_xlabel("$x_1$")
        a.set_ylabel("$x_2$")
    
    plt.suptitle("Влияние параметра качества $t$ на распределение точек", fontsize=15, y=1.05)
    plt.tight_layout()
    save_figure(fig, "fig_quality_parameter_t.pdf", output_dir)


def plot_owen_scrambling_visual(output_dir: Path) -> None:
    """
    Рисунок 5.1: Сравнение детерминированной и скремблированной сети Соболя.
    """
    logger.info("Генерация: fig_owen_scrambling_visual.pdf")
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    N = 64
    dim = 2
    
    # Детерминированная сеть
    sobol_det = qmc.Sobol(d=dim, seed=None)
    pts_det = sobol_det.random(N)
    
    # Скремблированная сеть
    sobol_rand = qmc.Sobol(d=dim, scramble=True, seed=42)
    pts_rand = sobol_rand.random(N)
    
    axes[0].scatter(pts_det[:, 0], pts_det[:, 1], s=20, c=COLORS["qmc"], alpha=0.7)
    axes[0].set_title("Детерминированная сеть Соболя")
    axes[0].set_xlim(0, 1)
    axes[0].set_ylim(0, 1)
    axes[0].set_aspect("equal")
    axes[0].grid(True, linestyle=":", alpha=0.4)
    axes[0].set_xlabel("$x_1$")
    axes[0].set_ylabel("$x_2$")
    
    axes[1].scatter(pts_rand[:, 0], pts_rand[:, 1], s=20, c=COLORS["rqmc"], alpha=0.7)
    axes[1].set_title("Скремблированная сеть (Оуэн)")
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].set_aspect("equal")
    axes[1].grid(True, linestyle=":", alpha=0.4)
    axes[1].set_xlabel("$x_1$")
    axes[1].set_ylabel("$x_2$")
    
    plt.suptitle("Эффект скремблирования Оуэна: сохранение равномерности", fontsize=14, y=1.02)
    plt.tight_layout()
    save_figure(fig, "fig_owen_scrambling_visual.pdf", output_dir)


def plot_variance_convergence_comparison(output_dir: Path) -> None:
    """
    Рисунок 5.2: Сравнение сходимости дисперсии методов интегрирования.
    """
    logger.info("Генерация: fig_variance_convergence.pdf")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    np.random.seed(42)
    N_vals = np.array([2**k for k in range(4, 13)])
    R = 50
    dim = 5
    
    def f(x: np.ndarray) -> np.ndarray:
        return np.prod(1 + 0.5 * np.sin(2 * np.pi * x[:, :3]), axis=1)
    
    var_mc, var_qmc, var_rqmc = [], [], []
    
    for N in N_vals:
        # MC
        mc_est = [np.mean(f(np.random.rand(N, dim))) for _ in range(R)]
        var_mc.append(np.var(mc_est, ddof=1))
        
        # QMC
        true_val = 1.0
        qmc_est = []
        sobol = qmc.Sobol(d=dim)
        for _ in range(R):
            x = sobol.random(N)
            qmc_est.append(np.mean(f(x)))
        var_qmc.append(np.mean((np.array(qmc_est) - true_val)**2))
        
        # RQMC
        rqmc_est = []
        for _ in range(R):
            sobol_r = qmc.Sobol(d=dim, scramble=True, seed=np.random.randint(10**6))
            x = sobol_r.random(N)
            rqmc_est.append(np.mean(f(x)))
        var_rqmc.append(np.var(rqmc_est, ddof=1))
    
    ax.loglog(N_vals, var_mc, "o-", label=r"MC: $O(N^{-1})$",
              color=COLORS["mc"], markersize=4)
    ax.loglog(N_vals, var_qmc, "s--", label=r"QMC (дет.): $O(N^{-1}(\log N)^{s-1})$",
              color=COLORS["qmc"], markersize=4)
    ax.loglog(N_vals, var_rqmc, "^-", label=r"RQMC (Оуэн): $O(N^{-3})$",
              color=COLORS["rqmc"], markersize=4)
    
    # Референсные линии
    ref_N = np.array([N_vals[0], N_vals[-1]])
    ax.loglog(ref_N, [var_mc[0] * (n_val / ref_N[0])**(-1) for n_val in ref_N],
              "gray", linestyle=":", alpha=0.5, label=r"Склон $-1$")
    ax.loglog(ref_N, [var_rqmc[0] * (n_val / ref_N[0])**(-3) for n_val in ref_N],
              "coral", linestyle=":", alpha=0.5, label=r"Склон $-3$")
    
    ax.set_xlabel(r"Число точек $N$ (лог. шкала)")
    ax.set_ylabel(r"Эмпирическая дисперсия (лог. шкала)")
    ax.set_title("Сравнение сходимости дисперсии методов интегрирования")
    ax.grid(True, which="both", linestyle=":", alpha=0.4)
    ax.legend(fontsize=9)
    
    plt.tight_layout()
    save_figure(fig, "fig_variance_convergence.pdf", output_dir)


FIGURE_REGISTRY: Dict[str, Callable[[Path], None]] = {
    "fig_discrepancy_comparison": plot_discrepancy_comparison,
    "fig_function_variation": plot_function_variation,
    "fig_centred_lattice": plot_centred_lattice,
    "fig_elementary_intervals": plot_elementary_intervals,
    "fig_quality_parameter_t": plot_quality_parameter_t,
    "fig_owen_scrambling_visual": plot_owen_scrambling_visual,
    "fig_variance_convergence": plot_variance_convergence_comparison,
}

CHAPTER_MAPPING: Dict[int, List[str]] = {
    2: ["fig_discrepancy_comparison", "fig_function_variation", "fig_centred_lattice"],
    3: ["fig_elementary_intervals", "fig_quality_parameter_t"],
    4: ["fig_anova_decomposition_2d", "fig_effective_dimension_curves"],
    5: ["fig_owen_scrambling_visual", "fig_variance_convergence", "fig_confidence_intervals_clt"],
}


def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Генерация графиков для пособия по RQMC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --all                          # Сгенерировать все графики
  %(prog)s --chapter 2                    # Только графики Главы 2
  %(prog)s --figure fig_owen_scrambling   # Один конкретный график
  %(prog)s --all --output-dir ./output    # Свой каталог для сохранения
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all", action="store_true",
        help="Сгенерировать все доступные графики"
    )
    group.add_argument(
        "--chapter", type=int, choices=[2, 3, 4, 5],
        help="Сгенерировать графики для указанной главы"
    )
    group.add_argument(
        "--figure", type=str, choices=list(FIGURE_REGISTRY.keys()),
        help="Сгенерировать один конкретный график"
    )
    
    parser.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
        help=f"Директория для сохранения графиков (по умолчанию: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Включить подробный вывод (debug-уровень логирования)"
    )
    
    return parser.parse_args()


def main() -> int:
    """Точка входа."""
    args = parse_args()
    
    setup_logging(level=logging.DEBUG if args.verbose else logging.INFO)
    output_dir = ensure_directory(args.output_dir)
    
    logger.info(f"Директория вывода: {output_dir.resolve()}")
    
    # Определение списка графиков для генерации
    if args.all:
        figures_to_generate = list(FIGURE_REGISTRY.keys())
    elif args.chapter:
        figures_to_generate = CHAPTER_MAPPING.get(args.chapter, [])
    else:  # args.figure
        figures_to_generate = [args.figure]
    
    if not figures_to_generate:
        logger.error("Не выбраны графики для генерации")
        return 1
    
    logger.info(f"Запланировано графиков: {len(figures_to_generate)}")
    
    # Генерация
    errors = []
    for fig_name in figures_to_generate:
        try:
            func = FIGURE_REGISTRY[fig_name]
            func(output_dir)
        except Exception as e:
            logger.error(f"Ошибка при генерации {fig_name}: {e}", exc_info=True)
            errors.append(fig_name)
    
    # Отчёт
    if errors:
        logger.error(f"Не удалось сгенерировать {len(errors)} график(ов): {errors}")
        return 1
    
    logger.info(f"✓ Успешно сгенерировано {len(figures_to_generate)} график(ов)")
    return 0


if __name__ == "__main__":
    sys.exit(main())