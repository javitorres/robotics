import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import trimesh

scene_model = None
vertices = []
faces = []

class EstadoRobot:
    def __init__(self):
        self.hombro_angle = 0
        self.hombro_updown = 0
        self.codo_angle = 0
        self.codo_updown = 0
        self.muneca_angle = 0
        self.muneca_updown = 0

def cargar_modelo_gltf(ruta):
    global scene_model, vertices, faces
    scene_model = trimesh.load(ruta)

    if isinstance(scene_model, trimesh.Scene):
        # Es una escena, extraemos las geometrías
        combined = trimesh.util.concatenate(scene_model.dump())  # Juntamos todas las piezas
        vertices = combined.vertices
        faces = combined.faces
    elif isinstance(scene_model, trimesh.Trimesh):
        # Es una sola malla
        vertices = scene_model.vertices
        faces = scene_model.faces
    else:
        raise Exception("Formato de modelo no reconocido")


def draw_model():
    glBegin(GL_TRIANGLES)
    for face in faces:
        for idx in face:
            glVertex3fv(vertices[idx])
    glEnd()

def brazo_robotico(estado):
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

    glPopMatrix()

def draw_sphere(radius=0.15, slices=16, stacks=16):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)

def draw_cylinder(length=1.0, radius=0.1, slices=16):
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, radius, length, slices, 1)
    gluDeleteQuadric(quadric)

def main(estado):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glRotatef(20, 1, 0, 0)

    modelo = input("1 robot, cualquier otra cosa modelo basico: ")
    if modelo.strip()=="1":
        print("Modelo 3D cargado")
        cargar_modelo_gltf("3dmodels/robotic_arm.glb")
    else:
        print("Modelo basico '" + modelo + "'")


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
        if keys[pygame.K_w]:
            estado.hombro_updown += 2
        if keys[pygame.K_s]:
            estado.hombro_updown -= 2

        if keys[pygame.K_a]:
            estado.codo_angle += 2
        if keys[pygame.K_d]:
            estado.codo_angle -= 2
        if keys[pygame.K_q]:
            estado.codo_updown += 2
        if keys[pygame.K_e]:
            estado.codo_updown -= 2

        if keys[pygame.K_z]:
            estado.muneca_angle += 2
        if keys[pygame.K_c]:
            estado.muneca_angle -= 2
        if keys[pygame.K_r]:
            estado.muneca_updown += 2
        if keys[pygame.K_f]:
            estado.muneca_updown -= 2

        #Key instrctions:
        # Hombro: Izquierda/Derecha (K_LEFT/K_RIGHT), Arriba/Abajo (K_w/K_s)
        # Codo: Izquierda/Derecha (K_a/K_d), Arriba/Abajo (K_q/K_e)
        # Muñeca: Izquierda/Derecha (K_z/K_c), Arriba/Abajo (K_r/K_f)
        # Resetear ángulos (K_r)


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        if scene_model:
            # Aplicamos transformaciones
            glRotatef(estado.hombro_angle, 0, 1, 0)
            glRotatef(estado.hombro_updown, 1, 0, 0)
            glTranslatef(0, 0, 2)

            glRotatef(estado.codo_angle, 0, 1, 0)
            glRotatef(estado.codo_updown, 1, 0, 0)
            glTranslatef(0, 0, 1.5)

            glRotatef(estado.muneca_angle, 0, 1, 0)
            glRotatef(estado.muneca_updown, 1, 0, 0)

            draw_model()
        else:
            brazo_robotico(estado)

        glPopMatrix()

        pygame.display.flip()

