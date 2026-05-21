#!/usr/bin/env python3
"""Build GF(9) = F_3[x]/(x^2 + 1) addition and multiplication tables.

We work over F_3 = {0,1,2} with arithmetic mod 3.
In the quotient by (x^2 + 1), we have:

  x^2 ≡ -1 (mod 3) ≡ 2.

So for elements (a + b x) and (c + d x):

  (a + b x)(c + d x)
    = ac + (ad+bc)x + bd x^2
    ≡ (ac + 2bd) + (ad+bc)x   (mod 3).

The script prints addition and multiplication Cayley tables and performs
basic sanity checks (identities, inverses, commutativity, distributivity).

Usage:
  python3 gf9_tables.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple


MOD = 3


def mod3(n: int) -> int:
    return n % MOD


@dataclass(frozen=True, order=True)
class GF9:
    """An element a + b*x in GF(9) with coefficients in F_3."""

    a: int  # constant term
    b: int  # x coefficient

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", mod3(self.a))
        object.__setattr__(self, "b", mod3(self.b))

    def __add__(self, other: "GF9") -> "GF9":
        return GF9(self.a + other.a, self.b + other.b)

    def __neg__(self) -> "GF9":
        return GF9(-self.a, -self.b)

    def __sub__(self, other: "GF9") -> "GF9":
        return self + (-other)

    def __mul__(self, other: "GF9") -> "GF9":
        # (a + bx)(c + dx) = ac + (ad+bc)x + bd x^2, with x^2 = 2 in F_3
        a, b = self.a, self.b
        c, d = other.a, other.b
        const = a * c + 2 * b * d
        xcoef = a * d + b * c
        return GF9(const, xcoef)

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def label(self) -> str:
        """Pretty label for table headers."""
        a, b = self.a, self.b
        if b == 0:
            return f"{a}"
        if a == 0:
            if b == 1:
                return "x"
            return f"{b}x"
        if b == 1:
            return f"{a}+x"
        return f"{a}+{b}x"


def elements() -> List[GF9]:
    # Fixed order: 0,1,2,x,x+1,x+2,2x,2x+1,2x+2
    return [
        GF9(0, 0),
        GF9(1, 0),
        GF9(2, 0),
        GF9(0, 1),
        GF9(1, 1),
        GF9(2, 1),
        GF9(0, 2),
        GF9(1, 2),
        GF9(2, 2),
    ]


def build_table(els: List[GF9], op: str) -> List[List[GF9]]:
    if op not in {"+", "*"}:
        raise ValueError("op must be '+' or '*'")
    table: List[List[GF9]] = []
    for r in els:
        row: List[GF9] = []
        for c in els:
            row.append(r + c if op == "+" else r * c)
        table.append(row)
    return table


def print_table(els: List[GF9], table: List[List[GF9]], op_symbol: str) -> None:
    headers = [e.label() for e in els]
    # Choose a uniform column width for nice alignment.
    width = max(len(h) for h in headers)
    width = max(width, 3)

    def fmt(s: str) -> str:
        return s.rjust(width)

    print()
    print(f"{op_symbol} table for GF(9) with x^2 = 2 (mod 3)")
    print(fmt(op_symbol) + " | " + " ".join(fmt(h) for h in headers))
    print("-" * (width + 3 + (width + 1) * len(headers)))
    for r, row in zip(headers, table):
        print(fmt(r) + " | " + " ".join(fmt(x.label()) for x in row))


def find_identity(els: List[GF9], op: str) -> GF9 | None:
    for e in els:
        ok = True
        for a in els:
            if op == "+":
                ok = ok and (a + e == a) and (e + a == a)
            else:
                ok = ok and (a * e == a) and (e * a == a)
        if ok:
            return e
    return None


def inverse(a: GF9, els: List[GF9]) -> GF9 | None:
    one = GF9(1, 0)
    for b in els:
        if a * b == one and b * a == one:
            return b
    return None


def sanity_checks(els: List[GF9]) -> None:
    zero = find_identity(els, "+")
    one = find_identity(els, "*")
    if zero != GF9(0, 0):
        raise AssertionError(f"Additive identity expected 0, got {zero}")
    if one != GF9(1, 0):
        raise AssertionError(f"Multiplicative identity expected 1, got {one}")

    # Check x^2 == 2
    x = GF9(0, 1)
    if x * x != GF9(2, 0):
        raise AssertionError(f"Expected x^2 = 2, got {x * x}")

    # Commutativity
    for a in els:
        for b in els:
            if a + b != b + a:
                raise AssertionError("Addition is not commutative")
            if a * b != b * a:
                raise AssertionError("Multiplication is not commutative")

    # Distributivity
    for a in els:
        for b in els:
            for c in els:
                if a * (b + c) != (a * b) + (a * c):
                    raise AssertionError("Left distributivity failed")
                if (a + b) * c != (a * c) + (b * c):
                    raise AssertionError("Right distributivity failed")

    # Inverses for nonzero elements
    for a in els:
        if a.is_zero():
            continue
        inv = inverse(a, els)
        if inv is None:
            raise AssertionError(f"No inverse found for {a.label()}")


def main() -> None:
    els = elements()
    sanity_checks(els)

    add_table = build_table(els, "+")
    mul_table = build_table(els, "*")

    print_table(els, add_table, "+")
    print_table(els, mul_table, "×")


if __name__ == "__main__":
    main()

