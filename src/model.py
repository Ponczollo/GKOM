from dataclasses import dataclass


Vertex = tuple[float, float, float]
Face = tuple[tuple[int, ...], float]


@dataclass(frozen=True)
class Model:

    vertices: tuple[Vertex, ...]
    faces: tuple[Face, ...]

    @classmethod
    def unit_cube(cls) -> "Model":
        """Return a cube centred on X/Y with its base at Z = 0."""
        return cls(
            vertices=(
                (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0),
                (0.5, -0.5, 1.0), (-0.5, -0.5, 1.0),
                (-0.5, 0.5, 0.0), (0.5, 0.5, 0.0),
                (0.5, 0.5, 1.0), (-0.5, 0.5, 1.0),
            ),
            faces=(
                ((0, 3, 2, 1), 0.65), ((4, 5, 6, 7), 0.85),
                ((0, 4, 7, 3), 0.70), ((1, 2, 6, 5), 0.90),
                ((3, 7, 6, 2), 1.00), ((0, 1, 5, 4), 0.55),
            ),
        )
