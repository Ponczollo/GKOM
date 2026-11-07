from math import atan2, degrees

from src.base_entity import BaseEntity
from src.model import Model
from src.utils import Vector2


class Player(BaseEntity):

    def __init__(
        self,
        pos_x: float = 0.0,
        pos_y: float = 0.0,
        pos_z: float = 0.0,
        move_vector: Vector2 | None = None,
        model: Model | None = None,
    ) -> None:
        super().__init__(pos_x, pos_y, pos_z, move_vector, model)

    @property
    def model_rotation(self) -> float:
        """Z-axis rotation in degrees that points the model along its velocity."""
        if self.move_vector.length == 0:
            return 0.0
        return degrees(atan2(-self.move_vector.x, self.move_vector.y))
