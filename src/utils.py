from math import sqrt, sin, cos


class Vector2:

    _x: float = 0
    _y: float = 0
    _length: float = 0
    _limit: float = float('inf')

    def __init__(self, x: float, y: float, /):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def length(self):
        return self._length

    @property
    def limit(self):
        return self._limit

    @x.setter
    def x(self, value: float):
        self._x = value
        self._length = self._vector_value()
        if self._length > self.limit:
            self.length = self.limit

    @y.setter
    def y(self, value: float):
        self._y = value
        self._length = self._vector_value()
        if self._length > self.limit:
            self.length = self.limit

    @length.setter
    def length(self, value: float):
        ratio = value / self.length
        self.x *= ratio
        self.y *= ratio

    @limit.setter
    def limit(self, value: float):
        self._limit = value
        if self.length > self.limit:
            self.length = self.limit

    def __add__(self, other: Vector2):
        self.x += other.x
        self.y += other.y

    def _vector_value(self) -> float:
        retv = sqrt(self.x**2 + self.y**2)
        return retv

    def turn(self, angle: int):
        """
        Range is [-180, 180]
        - is right side turn
        + is left side turn
        """
        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        self.x = x
        self.y = y