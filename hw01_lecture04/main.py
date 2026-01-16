"""
Quadratic equation solver module.

This module provides a :class:`Solver` class for solving quadratic equations
of the form ax^2 + bx + c = 0, where a, b, and c are real finite numbers.
It handles edge cases such as zero discriminant, negative discriminant,
and invalid coefficients (non-numeric, infinite, or NaN values).
"""

import math


class QuadraticCoefficientZeroError(Exception):
    """
    Exception raised when the quadratic coefficient 'a' is zero.

    This error indicates that the given equation is not quadratic
    (it degenerates into a linear equation or constant).
    """


class NonNumericCoefError(Exception):
    """
    Exception raised when one or more coefficients are non-numeric,
    infinite, or NaN (Not a Number).

    The solver requires all coefficients to be finite real numbers.
    """


class Solver:
    """
    A solver for quadratic equations of the form ax^2 + bx + c = 0.

    Uses a small epsilon tolerance (1e-9) for floating-point comparisons
    to handle numerical inaccuracies. Only accepts finite numeric
    coefficients; raises exceptions otherwise.
    """

    EPSILON = 1e-9
    """float: Tolerance value used for floating-point comparisons."""

    @staticmethod
    def _d(a: float, b: float, c: float) -> float:
        """
        Compute the discriminant of a quadratic equation.

        :param a: Quadratic coefficient (must be finite float or int).
        :type a: float
        :param b: Linear coefficient (must be finite float or int).
        :type b: float
        :param c: Constant term (must be finite float or int).
        :type c: float
        :return: The discriminant value, D = b^2 - 4ac.
        :rtype: float
        """
        return b ** 2 - 4 * a * c
    
    @classmethod
    def solve(cls, a: float, b: float, c: float) -> list[float]:
        """
        Solve the quadratic equation ax^2 + bx + c = 0.

        :param a: Quadratic coefficient. Must be a finite number and non-zero.
        :type a: float
        :param b: Linear coefficient. Must be a finite number.
        :type b: float
        :param c: Constant term. Must be a finite number.
        :type c: float
        :returns: A list of real roots:
                  - Empty list if no real roots exist (D < 0),
                  - One-element list if one real root (D ≈ 0),
                  - Two-element list if two distinct real roots (D > 0).
        :rtype: list[float]
        :raises NonNumericCoefError: If any coefficient is non-numeric, infinite, or NaN.
        :raises AIsZeroError: If coefficient 'a' is zero (or close to zero within :attr:`EPSILON` tolerance).
        """
        if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in (a, b, c)):
            raise NonNumericCoefError("All coefficients must be finite numbers")
        
        if math.isclose(a, 0.0, abs_tol=cls.EPSILON):
            raise QuadraticCoefficientZeroError("Coefficient 'a' must be non-zero")
        
        d = cls._d(a, b, c)

        if d < -cls.EPSILON:
            return []
        
        if math.isclose(d, 0.0, abs_tol=cls.EPSILON):
            return [-b / (2 * a)]
        
        q = -0.5 * (b + math.copysign(math.sqrt(d), b))
        x1 = q / a
        x2 = c / q
        return [x1, x2]
