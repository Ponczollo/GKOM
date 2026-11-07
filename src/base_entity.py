from src.model import Model
from src.utils import Vector2


class BaseEntity:

    pos_x: float
    pos_y: float
    pos_z: float
    half_x: float
    half_y: float
    move_vector: Vector2
    model: Model | None

    def __init__(
        self,
        pos_x: float = 0.0,
        pos_y: float = 0.0,
        pos_z: float = 0.0,
        move_vector: Vector2 | None = None,
        model: Model | None = None,
        half_x: float = 0.5,
        half_y: float = 0.5,
    ) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.half_x = half_x
        self.half_y = half_y
        self.move_vector = move_vector or Vector2(0.0, 0.0)
        self.model = model

    def move(self, frametime: float) -> None:
        self.pos_x += self.move_vector.x * frametime
        self.pos_y += self.move_vector.y * frametime
