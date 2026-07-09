#!/usr/bin/env python3
"""Generate elliptic curve lecture images.

By default, this script uses the common toy curve

    y^2 = x^3 + 2x + 2

over the real numbers and over the finite field F_17. The curve parameters can
be changed with command-line options. The script saves one continuous real curve
image and one finite-field point image as PNG files.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError as exc:  # pragma: no cover - helpful runtime message
    raise SystemExit(
        "matplotlib is required. Install it with: python3 -m pip install matplotlib"
    ) from exc


DEFAULT_A = 2
DEFAULT_B = 2
DEFAULT_P = 17
DEFAULT_BASE_POINT = (5, 1)
DEFAULT_ANNOTATED_SCALARS = (1, 2, 3, 7)


@dataclass(frozen=True)
class CurveConfig:
    """Configuration for y^2 = x^3 + ax + b over R and F_p."""

    a: int
    b: int
    p: int
    x_min: float
    x_max: float
    sample_count: int
    output_prefix: str
    base_point: tuple[int, int] | None
    annotated_scalars: tuple[int, ...]


def curve_rhs_real(x: float, curve: CurveConfig) -> float:
    """Return x^3 + ax + b over the real numbers."""
    return x**3 + curve.a * x + curve.b


def curve_rhs_mod(x: int, curve: CurveConfig) -> int:
    """Return x^3 + ax + b modulo p."""
    return (x**3 + curve.a * x + curve.b) % curve.p


def is_prime(value: int) -> bool:
    """Return True if value is prime."""
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False

    factor = 3
    while factor * factor <= value:
        if value % factor == 0:
            return False
        factor += 2
    return True


def signed_term(coefficient: int, variable: str) -> str:
    """Format a signed polynomial term for labels."""
    if coefficient == 0:
        return ""

    sign = "+" if coefficient > 0 else "-"
    magnitude = abs(coefficient)
    coefficient_text = "" if magnitude == 1 and variable else str(magnitude)
    return f"{sign}{coefficient_text}{variable}"


def rhs_label(curve: CurveConfig) -> str:
    """Return a compact label for x^3 + ax + b."""
    return f"x^3{signed_term(curve.a, 'x')}{signed_term(curve.b, '')}"


def real_curve_samples(curve: CurveConfig) -> tuple[list[float], list[float], list[float]]:
    """Sample the real curve and return x-values plus upper/lower branches."""
    if curve.sample_count < 2:
        raise ValueError("sample_count must be at least 2.")

    xs: list[float] = []
    upper: list[float] = []
    lower: list[float] = []

    step = (curve.x_max - curve.x_min) / (curve.sample_count - 1)
    for index in range(curve.sample_count):
        x = curve.x_min + index * step
        y_squared = curve_rhs_real(x, curve)
        if y_squared >= 0:
            y = math.sqrt(y_squared)
            xs.append(x)
            upper.append(y)
            lower.append(-y)

    if not xs:
        raise ValueError("No real curve points were sampled. Adjust x_min and x_max.")

    return xs, upper, lower


def finite_field_points(curve: CurveConfig) -> list[tuple[int, int]]:
    """Enumerate all affine points satisfying y^2 = x^3 + ax + b mod p."""
    return [
        (x, y)
        for x in range(curve.p)
        for y in range(curve.p)
        if (y * y - curve_rhs_mod(x, curve)) % curve.p == 0
    ]


def mod_inverse(value: int, p: int) -> int:
    """Return the multiplicative inverse of value modulo p."""
    return pow(value % p, -1, p)


def point_add(
    point_a: tuple[int, int] | None,
    point_b: tuple[int, int] | None,
    curve: CurveConfig,
) -> tuple[int, int] | None:
    """Add two points on y^2 = x^3 + ax + b over F_p.

    The point at infinity is represented by None.
    """
    if point_a is None:
        return point_b
    if point_b is None:
        return point_a

    x1, y1 = point_a
    x2, y2 = point_b
    p = curve.p

    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if point_a == point_b:
        slope = ((3 * x1 * x1 + curve.a) * mod_inverse(2 * y1, p)) % p
    else:
        slope = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p

    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return x3, y3


def scalar_multiply(
    scalar: int,
    point: tuple[int, int],
    curve: CurveConfig,
) -> tuple[int, int] | None:
    """Compute scalar * point using double-and-add."""
    if scalar < 0:
        raise ValueError("Annotated scalars must be nonnegative.")

    result: tuple[int, int] | None = None
    addend: tuple[int, int] | None = point
    k = scalar

    while k > 0:
        if k & 1:
            result = point_add(result, addend, curve)
        addend = point_add(addend, addend, curve)
        k >>= 1

    return result


def validate_curve(curve: CurveConfig, points: list[tuple[int, int]]) -> None:
    """Validate the curve parameters and generated finite-field point set."""
    if curve.p <= 3:
        raise ValueError("p must be a prime greater than 3 for this short Weierstrass form.")
    if not is_prime(curve.p):
        raise ValueError(f"p must be prime; received p={curve.p}.")
    if curve.x_min >= curve.x_max:
        raise ValueError("x_min must be less than x_max.")

    real_discriminant = 4 * curve.a**3 + 27 * curve.b**2
    if real_discriminant == 0:
        raise ValueError("The real curve is singular.")

    modular_discriminant = real_discriminant % curve.p
    if modular_discriminant == 0:
        raise ValueError(f"The curve is singular modulo {curve.p}.")

    if not points:
        raise ValueError("No affine points were found for the curve over the finite field.")

    for x, y in points:
        if (y * y - curve_rhs_mod(x, curve)) % curve.p != 0:
            raise ValueError(f"Point {(x, y)} is not on the curve.")

    if curve.base_point is not None and curve.base_point not in points:
        raise ValueError(f"Base point {curve.base_point} is not on the curve modulo {curve.p}.")

    for scalar in curve.annotated_scalars:
        if scalar < 0:
            raise ValueError("Annotated scalars must be nonnegative.")


def setup_output_dir(path: Path) -> Path:
    """Create and return the output directory."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_real_curve(output_dir: Path, curve: CurveConfig) -> Path:
    """Create an image of the continuous real curve."""
    xs, upper, lower = real_curve_samples(curve)
    expression = rhs_label(curve)

    fig, ax = plt.subplots(figsize=(8, 6), dpi=160)
    ax.plot(xs, upper, color="#1f77b4", linewidth=2.5, label=fr"$y=+\sqrt{{{expression}}}$")
    ax.plot(xs, lower, color="#ff7f0e", linewidth=2.5, label=fr"$y=-\sqrt{{{expression}}}$")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    ax.set_title("Continuous Elliptic Curve over the Real Numbers")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(curve.x_min, curve.x_max)
    max_abs_y = max((abs(y) for y in upper), default=1)
    ax.set_ylim(-max_abs_y * 1.1, max_abs_y * 1.1)
    ax.legend(loc="upper left")
    ax.text(
        0.02,
        0.03,
        fr"$y^2={expression}$ over $\mathbb{{R}}$",
        transform=ax.transAxes,
        fontsize=11,
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85},
    )

    output_path = output_dir / f"{curve.output_prefix}_real_curve.png"
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def save_modular_points(
    output_dir: Path,
    curve: CurveConfig,
    points: list[tuple[int, int]],
) -> Path:
    """Create an image of the finite-field point set over F_p."""
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    expression = rhs_label(curve)

    fig, ax = plt.subplots(figsize=(8, 8), dpi=160)
    ax.scatter(xs, ys, s=95, color="#1f77b4", edgecolor="black", zorder=3)

    if curve.base_point is not None:
        annotated_points = {
            scalar: scalar_multiply(scalar, curve.base_point, curve)
            for scalar in curve.annotated_scalars
        }
        for scalar, point in annotated_points.items():
            if point is None:
                continue
            x, y = point
            label = "G" if scalar == 1 else f"{scalar}G"
            ax.scatter([x], [y], s=180, color="#d62728", edgecolor="black", zorder=4)
            ax.annotate(
                f"{label}={point}",
                xy=(x, y),
                xytext=(8, 8),
                textcoords="offset points",
                fontsize=10,
                bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85},
            )

    ax.set_title(fr"Discrete Points on the Same Curve over $\mathbb{{F}}_{{{curve.p}}}$")
    ax.set_xlabel(f"x mod {curve.p}")
    ax.set_ylabel(f"y mod {curve.p}")
    ax.set_xlim(-0.75, curve.p - 0.25)
    ax.set_ylim(-0.75, curve.p - 0.25)
    ax.set_aspect("equal", adjustable="box")
    if curve.p <= 31:
        ax.set_xticks(range(curve.p))
        ax.set_yticks(range(curve.p))
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.55)
    ax.text(
        0.02,
        0.98,
        fr"$y^2 \equiv {expression}\; (\mathrm{{mod}}\; {curve.p})$"
        f"\n{len(points)} affine points + $\\mathcal{{O}}$",
        transform=ax.transAxes,
        fontsize=11,
        verticalalignment="top",
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.9},
    )

    output_path = output_dir / f"{curve.output_prefix}_mod{curve.p}_points.png"
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate real and finite-field images for y^2 = x^3 + ax + b."
    )
    parser.add_argument("--a", type=int, default=DEFAULT_A, help="Curve coefficient a.")
    parser.add_argument("--b", type=int, default=DEFAULT_B, help="Curve coefficient b.")
    parser.add_argument("--p", type=int, default=DEFAULT_P, help="Prime modulus for the finite field.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory where PNG files will be written. Defaults to this script's folder.",
    )
    parser.add_argument(
        "--output-prefix",
        default="ecc",
        help="Prefix for generated PNG filenames.",
    )
    parser.add_argument("--x-min", type=float, default=-2.5, help="Minimum x-value for the real curve image.")
    parser.add_argument("--x-max", type=float, default=4.0, help="Maximum x-value for the real curve image.")
    parser.add_argument("--sample-count", type=int, default=1800, help="Number of samples for the real curve image.")
    parser.add_argument(
        "--base-point",
        type=int,
        nargs=2,
        metavar=("X", "Y"),
        default=DEFAULT_BASE_POINT,
        help="Base point to annotate on the finite-field image. Defaults to 5 1.",
    )
    parser.add_argument(
        "--no-base-point",
        action="store_true",
        help="Disable base-point and scalar-multiple annotations.",
    )
    parser.add_argument(
        "--annotated-scalars",
        type=int,
        nargs="*",
        default=DEFAULT_ANNOTATED_SCALARS,
        help="Scalars to annotate as multiples of the base point.",
    )
    return parser.parse_args()


def curve_from_args(args: argparse.Namespace) -> CurveConfig:
    """Create a curve configuration from command-line arguments."""
    base_point = None
    if not args.no_base_point:
        base_point = (args.base_point[0] % args.p, args.base_point[1] % args.p)

    return CurveConfig(
        a=args.a,
        b=args.b,
        p=args.p,
        x_min=args.x_min,
        x_max=args.x_max,
        sample_count=args.sample_count,
        output_prefix=args.output_prefix,
        base_point=base_point,
        annotated_scalars=tuple(args.annotated_scalars),
    )


def validate_outputs(paths: list[Path]) -> None:
    """Ensure generated image files exist and are not empty."""
    for path in paths:
        if not path.exists() or path.stat().st_size == 0:
            raise RuntimeError(f"Image was not generated correctly: {path}")


def main() -> None:
    args = parse_args()
    curve = curve_from_args(args)
    output_dir = setup_output_dir(args.output_dir)
    points = finite_field_points(curve)
    validate_curve(curve, points)

    generated_paths = [
        save_real_curve(output_dir, curve),
        save_modular_points(output_dir, curve, points),
    ]
    validate_outputs(generated_paths)


if __name__ == "__main__":
    main()

