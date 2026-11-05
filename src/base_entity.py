from src.utils import Vector2

class BaseEntity:
    
    pos_x: int
    pos_y: int
    pos_z: int
    move_vector: Vector2
    
    def __init__(self) -> None:
        ...

    def move(self, frametime) -> None:
        self.pos_x += self.move_vector * frametime
        self.pos_y += self.move_vector * frametime