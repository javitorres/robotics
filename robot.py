####### robot.py

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def distancia(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


class EstadoRobot:
    def __init__(self):
        self.hombro_angle = 0
        self.hombro_updown = 0
        self.codo_angle = 0
        self.codo_updown = 0
        self.muneca_angle = 0
        self.muneca_updown = 0
        self.pinza_opening = 0.2

        self.pelota_pos = [1.5, -0.8, 2.5]  # posición XYZ de la pelota
        self.pelota_agarrada = False  # indica si la pelota está agarrada


def brazo_robotico(estado):
    # Suelo
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glTranslatef(0, -1, 0)
    glScalef(5, 0.01, 5)  # plano ancho y delgado
    draw_cube()
    glPopMatrix()

    # Pelota
    glPushMatrix()
    glColor3f(1, 0.4, 0.1)

    if estado.pelota_agarrada:
        # Coloca la pelota al final de la pinza
        glTranslatef(0, 0, 0.5)  # final de muñeca
        glTranslatef(0, 0, 0.2)  # delante de los dedos
    else:
        glTranslatef(*estado.pelota_pos)

    draw_sphere(0.2)
    glPopMatrix()

    glPushMatrix()

    # Base
    glColor3f(0.5, 0.5, 0.5)
    draw_sphere(0.2)

    # Hombro
    glRotatef(estado.hombro_angle, 0, 1, 0)
    glRotatef(estado.hombro_updown, 1, 0, 0)
    glColor3f(0.2, 0.2, 1)
    draw_cylinder(2)

    # Codo
    glTranslatef(0, 0, 2)
    glColor3f(1, 0, 0)
    draw_sphere(0.2)

    glRotatef(estado.codo_angle, 0, 1, 0)
    glRotatef(estado.codo_updown, 1, 0, 0)
    glColor3f(0.2, 1, 0.2)
    draw_cylinder(1.5)

    # Muñeca
    glTranslatef(0, 0, 1.5)
    glColor3f(1, 1, 0)
    draw_sphere(0.15)

    glRotatef(estado.muneca_angle, 0, 1, 0)
    glRotatef(estado.muneca_updown, 1, 0, 0)
    glColor3f(1, 0.5, 0)
    draw_cylinder(0.5)

    # Pinza
    glTranslatef(0, 0, 0.5)  # Avanzamos al final de la muñeca
    glColor3f(1, 1, 1)

    # Dedo izquierdo
    glPushMatrix()
    glTranslatef(-estado.pinza_opening / 2, 0, 0)
    glScalef(0.05, 0.05, 0.2)
    draw_cube()
    glPopMatrix()

    # Dedo derecho
    glPushMatrix()
    glTranslatef(estado.pinza_opening / 2, 0, 0)
    glScalef(0.05, 0.05, 0.2)
    draw_cube()
    glPopMatrix()

    glPopMatrix()

def draw_sphere(radius=0.15, slices=16, stacks=16):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)

def draw_cylinder(length=1.0, radius=0.1, slices=16):
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, radius, length, slices, 1)
    gluDeleteQuadric(quadric)

def draw_cube():
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )

    edges = (
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7)
    )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main(estado):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 10, 10, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.7, 0.7, 0.7, 1.0))
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


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

        if keys[pygame.K_LEFT]:
            estado.hombro_angle += 2
        if keys[pygame.K_RIGHT]:
            estado.hombro_angle -= 2
        if keys[pygame.K_s]:
            estado.hombro_updown += 2
        if keys[pygame.K_w]:
            estado.hombro_updown -= 2

        if keys[pygame.K_a]:
            estado.codo_angle += 2
        if keys[pygame.K_d]:
            estado.codo_angle -= 2
        if keys[pygame.K_q]:
            estado.codo_updown += 2
        if keys[pygame.K_e]:
            estado.codo_updown -= 2

        if keys[pygame.K_x]:
            estado.muneca_angle += 2
        if keys[pygame.K_c]:
            estado.muneca_angle -= 2
        if keys[pygame.K_r]:
            estado.muneca_updown += 2
        if keys[pygame.K_f]:
            estado.muneca_updown -= 2

        if keys[pygame.K_t]:  # Abrir pinza
            estado.pinza_opening = min(estado.pinza_opening + 0.01, 0.5)
        if keys[pygame.K_g]:  # Cerrar pinza
            estado.pinza_opening = max(estado.pinza_opening - 0.01, 0.0)

        # If Z zoom in
        if keys[pygame.K_z] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            glTranslatef(0, 0, 0.1)
        # if z zoom out
        elif keys[pygame.K_z]:
            glTranslatef(0, 0, -0.1)

        # If cursors move camera
        if keys[pygame.K_UP]:
            glTranslatef(0, 0.1, 0)
        if keys[pygame.K_DOWN]:
            glTranslatef(0, -0.1, 0)
        if keys[pygame.K_LEFT]:
            glTranslatef(-0.1, 0, 0)
        if keys[pygame.K_RIGHT]:
            glTranslatef(0.1, 0, 0)

        # If ESC is pressed, exit
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        #Key instrctions:
        # Hombro: Izquierda/Derecha (K_LEFT/K_RIGHT), Arriba/Abajo (K_w/K_s)
        # Codo: Izquierda/Derecha (K_a/K_d), Arriba/Abajo (K_q/K_e)
        # Muñeca: Izquierda/Derecha (K_z/K_c), Arriba/Abajo (K_r/K_f)
        # Resetear ángulos (K_r)

        # Obtener posición de la punta del brazo en coordenadas aproximadas
        # (esto es muy simplificado y no considera rotaciones reales)
        pinza_pos_aprox = [0, 0, 0]
        pinza_pos_aprox[0] = 0  # sin rotaciones reales por ahora
        pinza_pos_aprox[1] = 0  # simplificado
        pinza_pos_aprox[2] = 2 + 1.5 + 0.5 + 0.2  # longitudes acumuladas de segmentos

        if not estado.pelota_agarrada and distancia(pinza_pos_aprox, estado.pelota_pos) < 0.4:
            if keys[pygame.K_y]:  # presiona Y para agarrar
                estado.pelota_agarrada = True

        if estado.pelota_agarrada and keys[pygame.K_u]:  # U para soltar
            estado.pelota_agarrada = False
            # Al soltar, actualiza posición de pelota con pinza
            estado.pelota_pos = list(pinza_pos_aprox)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glPushMatrix()

        brazo_robotico(estado)
        glPopMatrix()
        pygame.display.flip()
