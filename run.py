"""Simple OpenGL scene. Run with `python run.py`; R resets, Escape exits."""

import glfw
from OpenGL import GL, GLU


WIDTH, HEIGHT = 1000, 700
MOVE_SPEED = 1.0  # World units per second, along the positive Y axis.
START_Y = 0.0
VIEW_HALF_HEIGHT = 9.0
CAMERA_DISTANCE = 12.0
OBSTACLES = [(-3, 4), (2, 7), (-4, 11), (3, 15), (-2, 19)]

# Unit cube centered on X/Y, with its bottom at Z = 0 (Z is up).
VERTICES = [
    (-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, -0.5, 1), (-0.5, -0.5, 1),
    (-0.5, 0.5, 0), (0.5, 0.5, 0), (0.5, 0.5, 1), (-0.5, 0.5, 1),
]
FACES = [
    ((0, 3, 2, 1), 0.65), ((4, 5, 6, 7), 0.85),
    ((0, 4, 7, 3), 0.70), ((1, 2, 6, 5), 0.90),
    ((3, 7, 6, 2), 1.00), ((0, 1, 5, 4), 0.55),
]


def draw_cube(x, y, color):
    GL.glPushMatrix()
    GL.glTranslatef(x, y, 0)
    GL.glBegin(GL.GL_QUADS)
    for indices, shade in FACES:
        GL.glColor3f(*(component * shade for component in color))
        for index in indices:
            GL.glVertex3f(*VERTICES[index])
    GL.glEnd()
    GL.glPopMatrix()


def draw_ground(center_y):
    # Extend the visible patch as the camera advances; grid lines stay in world space.
    near_y = int(center_y) - 30
    far_y = int(center_y) + 30
    GL.glColor3f(0.28, 0.38, 0.28)
    GL.glBegin(GL.GL_QUADS)
    for vertex in [(-30, near_y, 0), (-30, far_y, 0), (30, far_y, 0), (30, near_y, 0)]:
        GL.glVertex3f(*vertex)
    GL.glEnd()

    # Lift the grid slightly above the ground to avoid depth flickering.
    GL.glColor3f(0.36, 0.46, 0.36)
    GL.glBegin(GL.GL_LINES)
    for x in range(-30, 31):
        GL.glVertex3f(x, near_y, 0.002)
        GL.glVertex3f(x, far_y, 0.002)
    for y in range(near_y, far_y + 1):
        GL.glVertex3f(-30, y, 0.002)
        GL.glVertex3f(30, y, 0.002)
    GL.glEnd()


def main():
    if not glfw.init():
        raise RuntimeError("Could not initialize GLFW; a graphical display is required.")

    try:
        # OpenGL 2.1 supports the fixed-function API used in this small example.
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        window = glfw.create_window(WIDTH, HEIGHT, "OpenGL cubes | R: reset | Esc: quit", None, None)
        if not window:
            raise RuntimeError("Could not create an OpenGL window.")
        glfw.make_context_current(window)
        glfw.swap_interval(1)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(0.55, 0.72, 0.88, 1.0)
        moving_y = START_Y
        previous_time = glfw.get_time()

        while not glfw.window_should_close(window):
            glfw.poll_events()
            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(window, True)

            now = glfw.get_time()
            delta_time = now - previous_time
            previous_time = now
            moving_y += MOVE_SPEED * delta_time
            if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS:
                moving_y = START_Y

            width, height = glfw.get_framebuffer_size(window)
            if width == 0 or height == 0:
                glfw.wait_events_timeout(0.1)
                continue

            GL.glViewport(0, 0, width, height)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            GL.glMatrixMode(GL.GL_PROJECTION)
            GL.glLoadIdentity()
            half_width = VIEW_HALF_HEIGHT * width / height
            GL.glOrtho(-half_width, half_width, -VIEW_HALF_HEIGHT, VIEW_HALF_HEIGHT, 0.1, 100)
            GL.glMatrixMode(GL.GL_MODELVIEW)
            GL.glLoadIdentity()
            # Equal X/Y/Z offsets give an isometric view from above and behind.
            GLU.gluLookAt(
                CAMERA_DISTANCE, moving_y - CAMERA_DISTANCE, CAMERA_DISTANCE + 0.5,
                0, moving_y, 0.5,
                0, 0, 1,
            )

            draw_ground(moving_y)
            for x, y in OBSTACLES:
                draw_cube(x, y, (0.20, 0.48, 0.85))
            draw_cube(0, moving_y, (1.0, 0.35, 0.08))
            glfw.swap_buffers(window)
    finally:
        glfw.terminate()


if __name__ == "__main__":
    main()
