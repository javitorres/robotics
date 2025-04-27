import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Inicialización de las articulaciones
hombro_angle = 0
hombro_updown = 0
codo_angle = 0
codo_updown = 0
muñeca_angle = 0
muñeca_updown = 0

# Funciones para dibujar partes del brazo
def draw_cylinder(length=1.0, radius=0.1, slices=16):
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, radius, length, slices, 1)
    gluDeleteQuadric(quadric)

def draw_sphere(radius=0.15, slices=16, stacks=16):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)

def brazo_robotico():
    global hombro_angle, hombro_updown, codo_angle, codo_updown, muñeca_angle, muñeca_updown

    glPushMatrix()

    # Base fija
    glColor3f(0.5, 0.5, 0.5)
    draw_sphere(0.2)

    # Primer brazo (hombro)
    glRotatef(hombro_angle, 0, 1, 0)  # Giro izquierda/derecha
    glRotatef(hombro_updown, 1, 0, 0)  # Movimiento arriba/abajo
    glColor3f(0.2, 0.2, 1)
    draw_cylinder(2)

    # Codo
    glTranslatef(0, 0, 2)
    glColor3f(1, 0, 0)
    draw_sphere(0.2)

    # Segundo brazo (antebrazo)
    glRotatef(codo_angle, 0, 1, 0)  # Giro izquierda/derecha en codo
    glRotatef(codo_updown, 1, 0, 0)  # Movimiento arriba/abajo en codo
    glColor3f(0.2, 1, 0.2)
    draw_cylinder(1.5)

    # Muñeca
    glTranslatef(0, 0, 1.5)
    glColor3f(1, 1, 0)
    draw_sphere(0.15)

    # Movimiento de muñeca
    glRotatef(muñeca_angle, 0, 1, 0)
    glRotatef(muñeca_updown, 1, 0, 0)
    glColor3f(1, 0.5, 0)
    draw_cylinder(0.5)

    glPopMatrix()

def main():
    global hombro_angle, hombro_updown, codo_angle, codo_updown, muñeca_angle, muñeca_updown

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glRotatef(20, 1, 0, 0)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        # Hombro control
        if keys[pygame.K_LEFT]:
            hombro_angle += 2
        if keys[pygame.K_RIGHT]:
            hombro_angle -= 2
        if keys[pygame.K_w]:
            hombro_updown += 2
        if keys[pygame.K_s]:
            hombro_updown -= 2

        # Codo control
        if keys[pygame.K_a]:
            codo_angle += 2
        if keys[pygame.K_d]:
            codo_angle -= 2
        if keys[pygame.K_q]:
            codo_updown += 2
        if keys[pygame.K_e]:
            codo_updown -= 2

        # Muñeca control
        if keys[pygame.K_z]:
            muñeca_angle += 2
        if keys[pygame.K_c]:
            muñeca_angle -= 2
        if keys[pygame.K_r]:
            muñeca_updown += 2
        if keys[pygame.K_f]:
            muñeca_updown -= 2

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        brazo_robotico()
        pygame.display.flip()

if __name__ == "__main__":
    main()