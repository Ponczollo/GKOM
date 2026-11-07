"""Main game loop and OpenGL scene setup."""

import logging
import time

import glfw
from OpenGL import GL, GLU

from src.base_entity import BaseEntity
from src.model import Model
from src.player import Player
from src.renderer import Renderer
from src.utils import Vector2


logger = logging.getLogger(__name__)

WIDTH, HEIGHT = 1000, 700
FORWARD_SPEED = 3.0
TURN_SPEED = 120.0  # degrees per second
VIEW_HALF_HEIGHT = 9.0
CAMERA_DISTANCE = 12.0
CAMERA_HEIGHT = 12.5
OBSTACLE_POSITIONS = [(-3, 4), (2, 7), (-4, 11), (3, 15), (-2, 19)]


class MainGame:

    player: Player
    objects: list[BaseEntity]

    def __init__(self) -> None:
        self.window = None
        self.renderer = Renderer()

    def run(self) -> None:
        self.initialize()
        assert self.window is not None
        previous_time = glfw.get_time()
        frame_number = 1

        try:
            while not glfw.window_should_close(self.window):
                now = glfw.get_time()
                frametime = now - previous_time
                previous_time = now

                glfw.poll_events()
                self.handle_movement(frametime)
                self.handle_interactions()
                render_start = time.monotonic()
                self.render()
                render_time = time.monotonic() - render_start
                logger.debug(f"Frame {frame_number} rendered in {round(render_time * 1000, 2)}ms | {1 // render_time} fps")
                frame_number += 1
        finally:
            glfw.terminate()

    def initialize(self) -> None:
        if not glfw.init():
            raise RuntimeError("Could not initialize GLFW; a graphical display is required.")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        self.window = glfw.create_window(
            WIDTH,
            HEIGHT,
            "MonkeySwing | A/D: steer | L mouse: grapple | R: reset | Esc: quit",
            None,
            None,
        )
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Could not create an OpenGL window.")

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(0.55, 0.72, 0.88, 1.0)

        cube_model = Model.unit_cube()
        self.player = Player(move_vector=Vector2(0.0, FORWARD_SPEED), model=cube_model)
        self.objects = [
            BaseEntity(pos_x=x, pos_y=y, model=cube_model)
            for x, y in OBSTACLE_POSITIONS
        ]

    def handle_movement(self, frametime: float) -> None:
        """ Also handles inputs """
        assert self.window is not None

        # QUIT
        if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

        # STEERING
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.player.move_vector.turn(TURN_SPEED * frametime)
        elif glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.player.move_vector.turn(-TURN_SPEED * frametime)

        self.movement_calculation(frametime)

        if glfw.get_key(self.window, glfw.KEY_R) == glfw.PRESS:
            self.player.pos_x = 0.0
            self.player.pos_y = 0.0

    def movement_calculation(self, frametime: float) -> None:
        next_x = self.player.pos_x + self.player.move_vector.x * frametime
        if self.position_is_clear(next_x, self.player.pos_y):
            self.player.pos_x = next_x
        else:
            self.player.move_vector.x = 0.0

        next_y = self.player.pos_y + self.player.move_vector.y * frametime
        if self.position_is_clear(self.player.pos_x, next_y):
            self.player.pos_y = next_y
        else:
            self.player.move_vector.y = 0.0

    def position_is_clear(self, pos_x: float, pos_y: float) -> bool:
        """ Check if player/other entity doesnt collide with game objects """
        return not any(
            abs(pos_x - game_object.pos_x) < self.player.half_x + game_object.half_x
            and abs(pos_y - game_object.pos_y) < self.player.half_y + game_object.half_y
            for game_object in self.objects
        )

    def handle_interactions(self) -> None:
        """ Non-movement gameplay events - pickups, enemies collisions etc. """
        ...

    def render(self) -> None:
        """ Single frame render """
        assert self.window is not None
        width, height = glfw.get_framebuffer_size(self.window)
        if width == 0 or height == 0:
            return

        GL.glViewport(0, 0, width, height)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        half_width = VIEW_HALF_HEIGHT * width / height
        GL.glOrtho(-half_width, half_width, -VIEW_HALF_HEIGHT, VIEW_HALF_HEIGHT, 0.1, 100)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GLU.gluLookAt(
            self.player.pos_x,
            self.player.pos_y - CAMERA_DISTANCE,
            CAMERA_HEIGHT,
            self.player.pos_x,
            self.player.pos_y,
            0.5,
            0,
            0,
            1,
        )

        self._draw_ground(self.player.pos_y)
        for game_object in self.objects:
            self.renderer.draw(game_object, (0.20, 0.48, 0.85))
        self.renderer.draw(self.player, (1.0, 0.35, 0.08))
        glfw.swap_buffers(self.window)

    @staticmethod
    def _draw_ground(center_y: float) -> None:
        """
        Draw the visible ground patch and its world-space grid.
        TODO: Should be repllaced down the line
        """
        near_y = int(center_y) - 30
        far_y = int(center_y) + 30
        GL.glColor3f(0.28, 0.38, 0.28)
        GL.glBegin(GL.GL_QUADS)
        for vertex in [(-30, near_y, 0), (-30, far_y, 0), (30, far_y, 0), (30, near_y, 0)]:
            GL.glVertex3f(*vertex)
        GL.glEnd()

        GL.glColor3f(0.5, 0.5, 0.5)
        GL.glBegin(GL.GL_LINES)
        for x in range(-30, 31):
            GL.glVertex3f(x, near_y, 0.002)
            GL.glVertex3f(x, far_y, 0.002)
        for y in range(near_y, far_y + 1):
            GL.glVertex3f(-30, y, 0.002)
            GL.glVertex3f(30, y, 0.002)
        GL.glEnd()
