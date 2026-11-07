from OpenGL import GL

from src.base_entity import BaseEntity


class Renderer:
    # TODO: add "model -> mesh -> material" structure instead of texturing with only color
    def draw(self, entity: BaseEntity, color: tuple[float, float, float]) -> None:
        if entity.model is None:
            return

        GL.glPushMatrix()
        GL.glTranslatef(entity.pos_x, entity.pos_y, entity.pos_z)
        GL.glRotatef(getattr(entity, "model_rotation", 0.0), 0.0, 0.0, 1.0)
        GL.glBegin(GL.GL_QUADS)
        for indices, shade in entity.model.faces:
            GL.glColor3f(*(component * shade for component in color))
            for index in indices:
                GL.glVertex3f(*entity.model.vertices[index])
        GL.glEnd()
        GL.glPopMatrix()
