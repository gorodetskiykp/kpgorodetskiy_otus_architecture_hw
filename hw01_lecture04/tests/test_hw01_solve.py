import pytest

from hw01_lecture04.main import NonNumericCoefError, QuadraticCoefficientZeroError, Solver


def test_no_roots():
    # x ** 2 + 1 = 0
    # a = 1
    # b = 0
    # c = 1
    roots = Solver.solve(a=1, b=0, c=1)
    assert isinstance(roots, list)
    assert len(roots) == 0


def test_two_roots():
    # x ** 2 - 1 = 0
    # a = 1
    # b = 0
    # c = -1
    roots = Solver.solve(a=1, b=0, c=-1)
    assert isinstance(roots, list)
    assert roots == [-1.0, 1.0]


def test_one_roots():
    # x ** 2 + (2 + 1.0e-10) * x + 1 = 0
    # a = 1
    # b = 2 + 1.0e-10
    # c = 1
    # D ~ 4.0e-10 
    roots = Solver.solve(a=1, b=(2 + 1.0e-10), c=1)
    assert isinstance(roots, list)
    assert len(roots) == 1
    assert roots[0] == pytest.approx(-1.0, abs=1.0e-10)


def test_a_is_zero():
    with pytest.raises(QuadraticCoefficientZeroError):
        Solver.solve(a=0, b=1, c=1)


non_numeric_params = [
    (float("inf")),
    (float("-inf")),
    (float("nan")),
    (None),
    ("15.1"),
    ([1]),
]

@pytest.mark.parametrize("param", non_numeric_params)
def test_non_numeric_a(param):
    with pytest.raises(NonNumericCoefError, match="finite numbers"):
        Solver.solve(a=param, b=0, c=-1)


@pytest.mark.parametrize("param", non_numeric_params)
def test_non_numeric_b(param):
    with pytest.raises(NonNumericCoefError, match="finite numbers"):
        Solver.solve(a=1, b=param, c=-1)


@pytest.mark.parametrize("param", non_numeric_params)
def test_non_numeric_c(param):
    with pytest.raises(NonNumericCoefError, match="finite numbers"):
        Solver.solve(a=1, b=0, c=param)


def test_big_b():
    roots = Solver.solve(a=1, b=1e20, c=1)
    assert isinstance(roots, list)
    assert len(roots) == 2
    assert roots[0] == pytest.approx(-1e+20, abs=1.0e-15)
    assert roots[1] == pytest.approx(-1e-20, abs=1.0e-25)


@pytest.mark.parametrize("a, b, x1, x2", [
    (1, -1, 1.0, 0.0),
    (1, 1, -1.0, 0.0),
])
def test_two_roots_with_zero_root(a, b, x1, x2):
    roots = Solver.solve(a=a, b=b, c=0)
    assert isinstance(roots, list)
    assert len(roots) == 2
    assert roots[0] == x1
    assert roots[1] == x2


def test_negative_a():
    # -x ** 2 + 4 = 0 → x = ±2
    roots = Solver.solve(a=-1, b=0, c=4)
    assert set(roots) == {-2.0, 2.0}


def test_tiny_coefficients():
    with pytest.raises(QuadraticCoefficientZeroError):
        Solver.solve(a=1e-20, b=2e-20, c=1e-20)
