class Solver:

    @staticmethod
    def _d(a: float, b: float, c: float) -> float:
        return b ** 2 - 4 * a * c
    
    @classmethod
    def solve(cls, a: float, b: float, c: float) -> list[float]:
        d = cls._d(a, b, c)
        if d < 0:
            return []
        x1 = (-b + d ** 0.5) / (2 * a)
        if d == 0:
            return [x1]
        x2 = (-b - d ** 0.5) / (2 * a)
        return [x1, x2]
