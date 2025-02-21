# -------------------------------------------------------- #
#                     IMPORT LIBRARIES                     #
# -------------------------------------------------------- #
import os
import sys
import numpy as np
import math


# -------------------------------------------------------- #
import salome

salome.salome_init()

import GEOM
from salome.geom import geomBuilder

geompy = geomBuilder.New()

# ----------------------- INTERNAL ----------------------- #
res = 1e-3
res2 = 1e-5
# ---------- IMPORT VIRTUALENV PYTHON LIBRARIES ---------- #

sys.path.append("/home/fernando/.virtualenvs/exflow-env/lib/python3.8/site-packages")


# -------------------------------------------------------- #
#                        DIRECTORIES                       #
# -------------------------------------------------------- #
def makedir(directory_path):
    # Verificar se a pasta existe
    if not os.path.exists(directory_path):
        # Se não existir, cria a pasta
        os.makedirs(directory_path)
        # print(f"Pasta criada: {directory_path}")
    else:
        # Se existir, remove todos os arquivos, mas não as subpastas
        for root, dirs, files in os.walk(directory_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                # os.remove(file_path)
                # print(f"Arquivo removido: {file_path}")

        # print(f"Todos os arquivos foram removidos de: {directory_path}")


# -------------------------------------------------------- #
#                         PREAMBLE                         #
# -------------------------------------------------------- #
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# ---------------------- DIRECTORIES --------------------- #
basedir = "geometries/domain"
makedir(basedir)


# -------------------------------------------------------- #
#                        CREATE BOX                        #
# -------------------------------------------------------- #
width = 0.26
height = 0.06
depth = 0.01


def create_box(xmin=-0.060, xmax=0.200, ymin=-0.060, ymax=0.060, dz=0.01):
    # -------------------- dimensions -------------------- #
    dx = xmax - xmin
    dy = ymax - ymin

    # ----------------------- inlet ---------------------- #
    inlet = geompy.MakeFaceHW(dz, dy, 2)
    geompy.TranslateDXDYDZ(inlet, xmin, 0, 0)

    # ---------------------- outlet ---------------------- #
    outlet = geompy.MakeTranslation(inlet, dx, 0, 0)

    # ------------------------ top ----------------------- #
    top = geompy.MakeFaceHW(dz, dx, 3)
    geompy.TranslateDXDYDZ(top, xmin + dx / 2, dy / 2, 0)

    # ---------------------- bottom ---------------------- #
    bottom = geompy.MakeTranslation(top, 0, -dy, 0)

    # ----------------------- front ---------------------- #
    front1 = geompy.MakeFaceHW(dx, dy, 1)
    geompy.TranslateDXDYDZ(front1, dx / 2 + xmin, 0, dz / 2)

    # ----------------------- back ----------------------- #
    back1 = geompy.MakeTranslation(front1, 0, 0, -dz)

    # ---------------------------------------------------- #
    #                      EXPORTATION                     #
    # ---------------------------------------------------- #
    defaultdir = basedir + "/default"
    makedir(defaultdir)
    geompy.ExportSTL(inlet, os.path.join(defaultdir, "inlet.stl"), True, res, False)
    geompy.ExportSTL(outlet, os.path.join(defaultdir, "outlet.stl"), True, res, False)
    geompy.ExportSTL(top, os.path.join(defaultdir, "top.stl"), True, res, False)
    geompy.ExportSTL(bottom, os.path.join(defaultdir, "bottom.stl"), True, res, False)

    # ---------------------------------------------------- #
    return inlet, outlet, top, bottom, front1, back1


# -------------------------------------------------------- #

inlet, outlet, top, bottom, front1, back1 = create_box()


# -------------------------------------------------------- #
#                     AUXILIAR FUNCIONS                    #
# -------------------------------------------------------- #
# ---------------------- semicircle ---------------------- #
def create_semicircle(side="left", central=False):
    # ---------------------- vertex ---------------------- #
    v1 = geompy.MakeVertex(0, 1, 0)  # Vértice superior
    v3 = geompy.MakeVertex(0, -1, 0)  # Vértice inferior

    # Alterar a posição do v2 com base no lado
    if side == "left":
        v2 = geompy.MakeVertex(-1, 0, 0)  # Vértice à esquerda
    elif side == "right":
        v2 = geompy.MakeVertex(1, 0, 0)  # Vértice à direita
    else:
        raise ValueError("O argumento 'side' deve ser 'left' ou 'right'.")

    # -------------------- semicircle -------------------- #
    arc = geompy.MakeArc(v1, v2, v3)  # Arco do semicirculo
    vec = geompy.MakeVector(v3, v1)  # Vetor para a linha reta
    wire = geompy.MakeFuseList([arc, vec], True, True)  # Unir arco e linha reta

    # Retorno com base no argumento 'central'
    if central == False:
        return arc  # Retorna apenas o arco
    else:
        return wire  # Retorna o wire (domínio completo)


# ------------------------ circle ------------------------ #
def create_circle():
    # ---------------------- vertex ---------------------- #
    v1 = geompy.MakeVertex(0, 1, 0)
    v2 = geompy.MakeVertex(-1, 0, 0)
    v3 = geompy.MakeVertex(0, -1, 0)
    # -------------------- semicircle -------------------- #
    wire1 = geompy.MakeArc(v1, v2, v3)
    # ---------------------- mirror ---------------------- #
    wire2 = geompy.MakeRotation(wire1, OZ, 180 * math.pi / 180.0)
    return wire1, wire2


# ----------------- equilateral triangle ----------------- #
def create_equilateral_triangle():
    # ---------------------- vertex ---------------------- #
    v1 = geompy.MakeVertex(1, -np.sqrt(3) / 2, 0)
    v2 = geompy.MakeVertex(0, np.sqrt(3) / 2, 0)
    v3 = geompy.MakeVertex(-1, -np.sqrt(3) / 2, 0)
    v4 = geompy.MakeVertex(0, -np.sqrt(3) / 2, 0)
    # ----------------------- left ----------------------- #
    vec1 = geompy.MakeVector(v2, v3)
    vec2 = geompy.MakeVector(v3, v4)
    # ----------------------- right ---------------------- #
    vec3 = geompy.MakeVector(v4, v1)
    vec4 = geompy.MakeVector(v1, v2)
    # ---------------------------------------------------- #
    wire1 = geompy.MakeFuseList([vec1, vec2], True, True)
    wire2 = geompy.MakeFuseList([vec3, vec4], True, True)
    return wire1, wire2


# --------------------- side triangle -------------------- #
def create_side_triangle(side="left"):
    # ---------------------- vertex ---------------------- #
    v1 = geompy.MakeVertex(0, -1, 0)
    v2 = geompy.MakeVertex(0, 1, 0)
    if side == "left":
        v3 = geompy.MakeVertex(-np.sqrt(3), 0, 0)
    elif side == "right":
        v3 = geompy.MakeVertex(np.sqrt(3), 0, 0)
    # --------------------- triangle --------------------- #
    vec1 = geompy.MakeVector(v2, v3)
    vec2 = geompy.MakeVector(v3, v1)
    # ----------------------- fuse ----------------------- #
    wire = geompy.MakeFuseList([vec1, vec2], True, True)

    return wire


# -------------------- side rectangle -------------------- #
def create_side_rectangle(side="left"):
    # ---------------------- vertex ---------------------- #
    v1 = geompy.MakeVertex(0, -1, 0)
    v2 = geompy.MakeVertex(0, 1, 0)
    if side == "left":
        v3 = geompy.MakeVertex(-1, 1, 0)
        v4 = geompy.MakeVertex(-1, -1, 0)
    elif side == "right":
        v3 = geompy.MakeVertex(1, 1, 0)
        v4 = geompy.MakeVertex(1, -1, 0)
    # -------------------- equilateral ------------------- #
    vec1 = geompy.MakeVector(v2, v3)
    vec2 = geompy.MakeVector(v3, v4)
    vec3 = geompy.MakeVector(v4, v1)
    # ----------------------- fuse ----------------------- #
    wire = geompy.MakeFuseList([vec1, vec2, vec3], True, True)

    return wire


# ------------------------ square ------------------------ #
def create_square():
    # ---------------------- vertex ---------------------- #
    v1 = geompy.MakeVertex(0, -1, 0)
    v2 = geompy.MakeVertex(0, 1, 0)
    v3 = geompy.MakeVertex(-1, 1, 0)
    v4 = geompy.MakeVertex(-1, -1, 0)
    # -------------------- equilateral ------------------- #
    vec1 = geompy.MakeVector(v1, v2)
    vec2 = geompy.MakeVector(v2, v3)
    vec3 = geompy.MakeVector(v3, v4)
    vec4 = geompy.MakeVector(v4, v1)
    # ----------------------- fuse ----------------------- #
    wire = geompy.MakeFuseList([vec1, vec2, vec3, vec4], True, True)
    return wire


# ------------------------ rhombus ----------------------- #
def create_rhombus():
    # ---------------------- vertex ---------------------- #
    v1 = geompy.MakeVertex(0, -np.sqrt(2), 0)
    v2 = geompy.MakeVertex(np.sqrt(2), 0, 0)
    v3 = geompy.MakeVertex(0, np.sqrt(2), 0)
    v4 = geompy.MakeVertex(-np.sqrt(2), 0, 0)
    # --------------------- triangle --------------------- #
    vec1 = geompy.MakeVector(v1, v2)
    vec2 = geompy.MakeVector(v2, v3)
    # ---------------------------------------------------- #
    vec3 = geompy.MakeVector(v3, v4)
    vec4 = geompy.MakeVector(v4, v1)
    # ----------------------- fuse ----------------------- #
    wire1 = geompy.MakeFuseList([vec1, vec2], True, True)
    wire2 = geompy.MakeFuseList([vec3, vec4], True, True)
    return wire1, wire2


# --------------------- parallelogram -------------------- #
def create_parallelogram():
    # ---------------------- vertex ---------------------- #
    v1 = geompy.MakeVertex(0, -1, 0)
    v2 = geompy.MakeVertex(1, -1, 0)
    v3 = geompy.MakeVertex(0, 1, 0)
    v4 = geompy.MakeVertex(-1, 1, 0)
    # ----------------------- left ----------------------- #
    vec1 = geompy.MakeVector(v3, v4)
    vec2 = geompy.MakeVector(v4, v1)
    # ----------------------- right ---------------------- #
    vec3 = geompy.MakeVector(v1, v2)
    vec4 = geompy.MakeVector(v2, v3)
    # ---------------------------------------------------- #
    wire1 = geompy.MakeFuseList([vec1, vec2], True, True)
    wire2 = geompy.MakeFuseList([vec3, vec4], True, True)
    return wire1, wire2


# -------------------------------------------------------- #
#                      CREATE OBSTACLE                     #
# -------------------------------------------------------- #


# -------------------------------------------------------- #
#                       1. SEMICIRCLE                      #
# -------------------------------------------------------- #


def semicircle():

    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Stretch/compression factors
    rotation_angles = [
        0,
        15,
        30,
        45,
        60,
        75,
        90,
        105,
        120,
        135,
        150,
        165,
        180,
        75,
        90,
        105,
        120,
        135,
        150,
        165,
        180,
    ]
    # ---------------------------------------------------- #
    wire = create_semicircle(central=True)
    # ---------------------------------------------------- #
    # ---------------------------------------------------- #
    for k in stretch_factors:
        # ---------------------- stretch --------------------- #
        wire_stretched = geompy.MakeScaleAlongAxes(wire, O, k, 1, 1)

        # ---------------------- rotate ---------------------- #
        for t in rotation_angles:

            wire_rotated = geompy.Rotate(wire_stretched, OZ, -np.radians(t))

            # -------------- adjust the centroid ------------- #
            x0, y0, _ = geompy.PointCoordinates(geompy.MakeCDG(wire_rotated))
            wire_centered = geompy.TranslateDXDYDZ(wire_rotated, -x0, -y0, 0)

            # # -------------------- scaling ------------------- #
            xmin, xmax, ymin, ymax, _, _ = geompy.BoundingBox(wire_centered)
            dx = xmax - xmin
            dy = ymax - ymin
            scale = max(0.02 / dx, 0.02 / dy)
            wire_scaled = geompy.MakeScaleTransform(wire_centered, O, scale)

            # ------------------------------------------------ #
            #                   MAKING DOMAIN                  #
            # ------------------------------------------------ #
            obs_middle = geompy.MakeFaceWires([wire_scaled], 1)
            obs_front = geompy.MakeTranslation(obs_middle, 0, 0, depth / 2)
            obs_back = geompy.MakeTranslation(obs_middle, 0, 0, -depth / 2)
            wall = geompy.MakePrismVecH2Ways(wire_scaled, OZ, depth / 2)

            obstacle = geompy.MakeSolidFromConnectedFaces(
                [obs_back, obs_front, wall], True
            )
            # ---------------------------------------- #
            front = geompy.MakeCutList(front1, [obstacle], True)
            back = geompy.MakeCutList(back1, [obstacle], False)
            # -------------------------------------------- #

            # # ------------------------------------------------ #
            # #                      EXPORT                      #
            # # ------------------------------------------------ #
            name = f"semicircle_def{int(k*100):03d}_rot{int(t):03d}"
            geomdir = basedir + f"/geom_{name}"
            makedir(geomdir)
            geompy.ExportSTL(wall, os.path.join(geomdir, "wall.stl"), True, res2, False)
            geompy.ExportSTL(
                front, os.path.join(geomdir, "front.stl"), True, res2, False
            )
            geompy.ExportSTL(back, os.path.join(geomdir, "back.stl"), True, res2, False)


# -------------------------------------------------------- #
#                       2. ELLIPSOID                       #
# -------------------------------------------------------- #


def ellipsoid():
    # ---------------------- factors --------------------- #
    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Stretch/compression factors
    rotation_angles = [0, 15, 30, 45, 60, 75]  # Rotation angles
    # ---------------------- creation -------------------- #
    wire1, wire2 = create_circle()
    # ---------------------------------------------------- #
    for kl in stretch_factors:
        # ---------------------- stretch --------------------- #
        lw_stretched = geompy.MakeScaleAlongAxes(wire1, O, kl, 1, 1)

        for kr in stretch_factors:
            # ---------------------- stretch --------------------- #
            rw_stretched = geompy.MakeScaleAlongAxes(wire2, O, kr, 1, 1)
            #     # ------------------- fuse ------------------- #
            wire_stretched = geompy.MakeFuseList(
                [lw_stretched, rw_stretched], True, True
            )
            # ---------------------- rotate ---------------------- #
            for t in rotation_angles:
                if kl == 1.0 and kr == 1.0 and t != 0:
                    continue
                wire_rotated = geompy.Rotate(wire_stretched, OZ, -np.radians(t))

                # -------------- adjust the centroid ------------- #
                x0, y0, _ = geompy.PointCoordinates(geompy.MakeCDG(wire_rotated))
                wire_centered = geompy.TranslateDXDYDZ(wire_rotated, -x0, -y0, 0)

                # # -------------------- scaling ------------------- #
                xmin, xmax, ymin, ymax, _, _ = geompy.BoundingBox(wire_centered)
                dx = xmax - xmin
                dy = ymax - ymin
                scale = max(0.02 / dx, 0.02 / dy)
                wire_scaled = geompy.MakeScaleTransform(wire_centered, O, scale)

                #     # # -------------------- saving -------------------- #

                # ------------------------------------------------ #
                #                   MAKING DOMAIN                  #
                # ------------------------------------------------ #
                obs_middle = geompy.MakeFaceWires([wire_scaled], 1)
                obs_front = geompy.MakeTranslation(obs_middle, 0, 0, depth / 2)
                obs_back = geompy.MakeTranslation(obs_middle, 0, 0, -depth / 2)
                wall = geompy.MakePrismVecH2Ways(wire_scaled, OZ, depth / 2)

                obstacle = geompy.MakeSolidFromConnectedFaces(
                    [obs_back, obs_front, wall], True
                )
                # ---------------------------------------- #
                front = geompy.MakeCutList(front1, [obstacle], True)
                back = geompy.MakeCutList(back1, [obstacle], False)
                # -------------------------------------------- #

                # # ------------------------------------------------ #
                # #                      EXPORT                      #
                # # ------------------------------------------------ #
                name = f"ellipsoid_ldef{int(kl*100):03d}_rdef{int(kr*100):03d}_rot{int(t):03d}"
                geomdir = basedir + f"/geom_{name}"
                makedir(geomdir)
                geompy.ExportSTL(
                    wall, os.path.join(geomdir, "wall.stl"), True, res2, False
                )
                geompy.ExportSTL(
                    front, os.path.join(geomdir, "front.stl"), True, res2, False
                )
                geompy.ExportSTL(
                    back, os.path.join(geomdir, "back.stl"), True, res2, False
                )


# -------------------------------------------------------- #
#                        3. TRIANGLE                       #
# -------------------------------------------------------- #
def triangle():

    stretch_factors = [0.75, 1.0, 1.5, 2.0]
    rotation_angles = [0, 10, 20, 30, 40, 50, 60, 75, 90, 105, 120]
    # ---------------------------------------------------- #
    wire1, wire2 = create_equilateral_triangle()
    # ---------------------------------------------------- #
    # ---------------------------------------------------- #
    for kl in stretch_factors:
        # ---------------------- stretch --------------------- #
        lw_stretched = geompy.MakeScaleAlongAxes(wire1, O, kl, 1, 1)

        for kr in stretch_factors:
            # ---------------------- stretch --------------------- #
            rw_stretched = geompy.MakeScaleAlongAxes(wire2, O, kr, 1, 1)
            #     # ------------------- fuse ------------------- #
            wire_stretched = geompy.MakeFuseList(
                [lw_stretched, rw_stretched], True, True
            )
            # ---------------------- rotate ---------------------- #
            for t in rotation_angles:

                wire_rotated = geompy.Rotate(wire_stretched, OZ, -np.radians(t))

                # -------------- adjust the centroid ------------- #
                x0, y0, _ = geompy.PointCoordinates(geompy.MakeCDG(wire_rotated))
                wire_centered = geompy.TranslateDXDYDZ(wire_rotated, -x0, -y0, 0)

                # # -------------------- scaling ------------------- #
                xmin, xmax, ymin, ymax, _, _ = geompy.BoundingBox(wire_centered)
                dx = xmax - xmin
                dy = ymax - ymin
                scale = max(0.02 / dx, 0.02 / dy)
                wire_scaled = geompy.MakeScaleTransform(wire_centered, O, scale)

                #     # # -------------------- saving -------------------- #

                # ------------------------------------------------ #
                #                   MAKING DOMAIN                  #
                # ------------------------------------------------ #
                obs_middle = geompy.MakeFaceWires([wire_scaled], 1)
                obs_front = geompy.MakeTranslation(obs_middle, 0, 0, depth / 2)
                obs_back = geompy.MakeTranslation(obs_middle, 0, 0, -depth / 2)
                wall = geompy.MakePrismVecH2Ways(wire_scaled, OZ, depth / 2)

                obstacle = geompy.MakeSolidFromConnectedFaces(
                    [obs_back, obs_front, wall], True
                )
                # ---------------------------------------- #
                front = geompy.MakeCutList(front1, [obstacle], True)
                back = geompy.MakeCutList(back1, [obstacle], False)
                # -------------------------------------------- #

                # # ------------------------------------------------ #
                # #                      EXPORT                      #
                # # ------------------------------------------------ #
                name = f"triangle_ldef{int(kl*100):03d}_rdef{int(kr*100):03d}_rot{int(t):03d}"
                geomdir = basedir + f"/geom_{name}"
                makedir(geomdir)
                geompy.ExportSTL(
                    wall, os.path.join(geomdir, "wall.stl"), True, res2, False
                )
                geompy.ExportSTL(
                    front, os.path.join(geomdir, "front.stl"), True, res2, False
                )
                geompy.ExportSTL(
                    back, os.path.join(geomdir, "back.stl"), True, res2, False
                )


# -------------------------------------------------------- #
#                       4A. RECTANGLE                      #
# -------------------------------------------------------- #
def rectangle():

    stretch_factors = [0.75, 1.0, 1.5, 2.0]
    rotation_angles = [0, 15, 30, 45, 60, 75]
    # ---------------------------------------------------- #
    wire = create_square()
    # ---------------------------------------------------- #
    # ---------------------------------------------------- #
    for k in stretch_factors:
        # ---------------------- stretch --------------------- #
        wire_stretched = geompy.MakeScaleAlongAxes(wire, O, k, 1, 1)

        # ---------------------- rotate ---------------------- #
        for t in rotation_angles:

            wire_rotated = geompy.Rotate(wire_stretched, OZ, -np.radians(t))

            # -------------- adjust the centroid ------------- #
            x0, y0, _ = geompy.PointCoordinates(geompy.MakeCDG(wire_rotated))
            wire_centered = geompy.TranslateDXDYDZ(wire_rotated, -x0, -y0, 0)

            # # -------------------- scaling ------------------- #
            xmin, xmax, ymin, ymax, _, _ = geompy.BoundingBox(wire_centered)
            dx = xmax - xmin
            dy = ymax - ymin
            scale = max(0.02 / dx, 0.02 / dy)
            wire_scaled = geompy.MakeScaleTransform(wire_centered, O, scale)

            # ------------------------------------------------ #
            #                   MAKING DOMAIN                  #
            # ------------------------------------------------ #
            obs_middle = geompy.MakeFaceWires([wire_scaled], 1)
            obs_front = geompy.MakeTranslation(obs_middle, 0, 0, depth / 2)
            obs_back = geompy.MakeTranslation(obs_middle, 0, 0, -depth / 2)
            wall = geompy.MakePrismVecH2Ways(wire_scaled, OZ, depth / 2)

            obstacle = geompy.MakeSolidFromConnectedFaces(
                [obs_back, obs_front, wall], True
            )
            # ---------------------------------------- #
            front = geompy.MakeCutList(front1, [obstacle], True)
            back = geompy.MakeCutList(back1, [obstacle], False)
            # -------------------------------------------- #

            # # ------------------------------------------------ #
            # #                      EXPORT                      #
            # # ------------------------------------------------ #
            name = f"square_def{int(k*100):03d}_rot{int(t):03d}"
            geomdir = basedir + f"/geom_{name}"
            makedir(geomdir)
            geompy.ExportSTL(wall, os.path.join(geomdir, "wall.stl"), True, res2, False)
            geompy.ExportSTL(
                front, os.path.join(geomdir, "front.stl"), True, res2, False
            )
            geompy.ExportSTL(back, os.path.join(geomdir, "back.stl"), True, res2, False)


# -------------------------------------------------------- #
#                        4B. RHOMBUS                       #
# -------------------------------------------------------- #
def rhombus():

    stretch_factors = [0.75, 1.0, 1.5, 2.0]
    rotation_angles = [0, 15, 30, 45, 60, 75]
    # ---------------------------------------------------- #
    wire1, wire2 = create_rhombus()
    # ---------------------------------------------------- #
    # ---------------------------------------------------- #
    for kl in stretch_factors:
        # ---------------------- stretch --------------------- #
        lw_stretched = geompy.MakeScaleAlongAxes(wire1, O, kl, 1, 1)

        for kr in stretch_factors:
            if kl == 1.0 and kr == 1.0:
                continue
            # ---------------------- stretch --------------------- #
            rw_stretched = geompy.MakeScaleAlongAxes(wire2, O, kr, 1, 1)
            #     # ------------------- fuse ------------------- #
            wire_stretched = geompy.MakeFuseList(
                [lw_stretched, rw_stretched], True, True
            )
            # ---------------------- rotate ---------------------- #
            for t in rotation_angles:

                wire_rotated = geompy.Rotate(wire_stretched, OZ, -np.radians(t))

                # -------------- adjust the centroid ------------- #
                x0, y0, _ = geompy.PointCoordinates(geompy.MakeCDG(wire_rotated))
                wire_centered = geompy.TranslateDXDYDZ(wire_rotated, -x0, -y0, 0)

                # # -------------------- scaling ------------------- #
                xmin, xmax, ymin, ymax, _, _ = geompy.BoundingBox(wire_centered)
                dx = xmax - xmin
                dy = ymax - ymin
                scale = max(0.02 / dx, 0.02 / dy)
                wire_scaled = geompy.MakeScaleTransform(wire_centered, O, scale)

                #     # # -------------------- saving -------------------- #

                # ------------------------------------------------ #
                #                   MAKING DOMAIN                  #
                # ------------------------------------------------ #
                obs_middle = geompy.MakeFaceWires([wire_scaled], 1)
                obs_front = geompy.MakeTranslation(obs_middle, 0, 0, depth / 2)
                obs_back = geompy.MakeTranslation(obs_middle, 0, 0, -depth / 2)
                wall = geompy.MakePrismVecH2Ways(wire_scaled, OZ, depth / 2)

                obstacle = geompy.MakeSolidFromConnectedFaces(
                    [obs_back, obs_front, wall], True
                )
                # ---------------------------------------- #
                front = geompy.MakeCutList(front1, [obstacle], True)
                back = geompy.MakeCutList(back1, [obstacle], False)
                # -------------------------------------------- #

                # # ------------------------------------------------ #
                # #                      EXPORT                      #
                # # ------------------------------------------------ #
                name = f"rhombus_ldef{int(kl*100):03d}_rdef{int(kr*100):03d}_rot{int(t):03d}"
                geomdir = basedir + f"/geom_{name}"
                makedir(geomdir)
                geompy.ExportSTL(
                    wall, os.path.join(geomdir, "wall.stl"), True, res2, False
                )
                geompy.ExportSTL(
                    front, os.path.join(geomdir, "front.stl"), True, res2, False
                )
                geompy.ExportSTL(
                    back, os.path.join(geomdir, "back.stl"), True, res2, False
                )


# -------------------------------------------------------- #
#                     4C. PARALLELOGRAM                    #
# -------------------------------------------------------- #
def parallelogram():

    stretch_factors = [0.75, 1.0, 1.5, 2.0]
    rotation_angles = [0, 15, 30, 45, 60, 75]
    # ---------------------------------------------------- #
    wire1, wire2 = create_parallelogram()
    # ---------------------------------------------------- #
    # ---------------------------------------------------- #
    for kl in stretch_factors:
        # ---------------------- stretch --------------------- #
        lw_stretched = geompy.MakeScaleAlongAxes(wire1, O, kl, 1, 1)

        for kr in stretch_factors:
            # ---------------------- stretch --------------------- #
            rw_stretched = geompy.MakeScaleAlongAxes(wire2, O, kr, 1, 1)
            #     # ------------------- fuse ------------------- #
            wire_stretched = geompy.MakeFuseList(
                [lw_stretched, rw_stretched], True, True
            )
            # ---------------------- rotate ---------------------- #
            for t in rotation_angles:

                wire_rotated = geompy.Rotate(wire_stretched, OZ, -np.radians(t))

                # -------------- adjust the centroid ------------- #
                x0, y0, _ = geompy.PointCoordinates(geompy.MakeCDG(wire_rotated))
                wire_centered = geompy.TranslateDXDYDZ(wire_rotated, -x0, -y0, 0)

                # # -------------------- scaling ------------------- #
                xmin, xmax, ymin, ymax, _, _ = geompy.BoundingBox(wire_centered)
                dx = xmax - xmin
                dy = ymax - ymin
                scale = max(0.02 / dx, 0.02 / dy)
                wire_scaled = geompy.MakeScaleTransform(wire_centered, O, scale)

                #     # # -------------------- saving -------------------- #

                # ------------------------------------------------ #
                #                   MAKING DOMAIN                  #
                # ------------------------------------------------ #
                obs_middle = geompy.MakeFaceWires([wire_scaled], 1)
                obs_front = geompy.MakeTranslation(obs_middle, 0, 0, depth / 2)
                obs_back = geompy.MakeTranslation(obs_middle, 0, 0, -depth / 2)
                wall = geompy.MakePrismVecH2Ways(wire_scaled, OZ, depth / 2)

                obstacle = geompy.MakeSolidFromConnectedFaces(
                    [obs_back, obs_front, wall], True
                )
                # ---------------------------------------- #
                front = geompy.MakeCutList(front1, [obstacle], True)
                back = geompy.MakeCutList(back1, [obstacle], False)
                # -------------------------------------------- #

                # # ------------------------------------------------ #
                # #                      EXPORT                      #
                # # ------------------------------------------------ #
                name = f"parallelogram_ldef{int(kl*100):03d}_rdef{int(kr*100):03d}_rot{int(t):03d}"
                geomdir = basedir + f"/geom_{name}"
                makedir(geomdir)
                geompy.ExportSTL(
                    wall, os.path.join(geomdir, "wall.stl"), True, res2, False
                )
                geompy.ExportSTL(
                    front, os.path.join(geomdir, "front.stl"), True, res2, False
                )
                geompy.ExportSTL(
                    back, os.path.join(geomdir, "back.stl"), True, res2, False
                )


def quadrilateral():
    rectangle()
    rhombus()
    parallelogram()


# -------------------------------------------------------- #
#                5. COMBINED CIRCLE TRIANGLE               #
# -------------------------------------------------------- #


def combined_shapes():
    stretch_factors = [0.75, 1.0, 1.5, 2.0]
    rotation_angles = [0, 15, 30, 45, 60, 75]

    shape_functions = {
        "circle": create_semicircle,
        "triangle": create_side_triangle,
        "square": create_side_rectangle,
    }

    combinations = [
        ["circle", "triangle"],
        ["circle", "square"],
        ["triangle", "square"],
    ]

    # Loop para percorrer as combinações
    for shape1, shape2 in combinations:
        for side1, side2 in [("left", "right"), ("right", "left")]:
            prefix = (
                f"{shape1[:3]}-{shape2[:3]}"
                if side1 == "left"
                else f"{shape2[:3]}-{shape1[:3]}"
            )

            # Garantindo que wire1 sempre corresponda à forma à esquerda e wire2 à forma à direita
            wire1 = shape_functions[shape1](side=side1)  # Forma à esquerda
            wire2 = shape_functions[shape2](side=side2)  # Forma à direita

            # ------------------- loop ------------------- #
            for kl in stretch_factors:
                # ---------------------- stretch --------------------- #
                lw_stretched = geompy.MakeScaleAlongAxes(wire1, O, kl, 1, 1)

                for kr in stretch_factors:
                    # ---------------------- stretch --------------------- #
                    rw_stretched = geompy.MakeScaleAlongAxes(wire2, O, kr, 1, 1)
                    #     # ------------------- fuse ------------------- #
                    wire_stretched = geompy.MakeFuseList(
                        [lw_stretched, rw_stretched], True, True
                    )
                    # ---------------------- rotate ---------------------- #
                    for t in rotation_angles:

                        wire_rotated = geompy.Rotate(wire_stretched, OZ, -np.radians(t))

                        # -------------- adjust the centroid ------------- #
                        x0, y0, _ = geompy.PointCoordinates(
                            geompy.MakeCDG(wire_rotated)
                        )
                        wire_centered = geompy.TranslateDXDYDZ(
                            wire_rotated, -x0, -y0, 0
                        )

                        # # -------------------- scaling ------------------- #
                        xmin, xmax, ymin, ymax, _, _ = geompy.BoundingBox(wire_centered)
                        dx = xmax - xmin
                        dy = ymax - ymin
                        scale = max(0.02 / dx, 0.02 / dy)
                        wire_scaled = geompy.MakeScaleTransform(wire_centered, O, scale)

                        #     # # -------------------- saving -------------------- #

                        # ------------------------------------------------ #
                        #                   MAKING DOMAIN                  #
                        # ------------------------------------------------ #
                        obs_middle = geompy.MakeFaceWires([wire_scaled], 1)
                        obs_front = geompy.MakeTranslation(obs_middle, 0, 0, depth / 2)
                        obs_back = geompy.MakeTranslation(obs_middle, 0, 0, -depth / 2)
                        wall = geompy.MakePrismVecH2Ways(wire_scaled, OZ, depth / 2)

                        obstacle = geompy.MakeSolidFromConnectedFaces(
                            [obs_back, obs_front, wall], True
                        )
                        # ---------------------------------------- #
                        front = geompy.MakeCutList(front1, [obstacle], True)
                        back = geompy.MakeCutList(back1, [obstacle], False)
                        # -------------------------------------------- #

                        # # ------------------------------------------------ #
                        # #                      EXPORT                      #
                        # # ------------------------------------------------ #
                        name = f"{prefix}_ldef{int(kr*100):03d}_rdef{int(kl*100):03d}_rot{int(t):03d}"
                        geomdir = basedir + f"/geom_{name}"
                        makedir(geomdir)
                        geompy.ExportSTL(
                            wall, os.path.join(geomdir, "wall.stl"), True, res2, False
                        )
                        geompy.ExportSTL(
                            front, os.path.join(geomdir, "front.stl"), True, res2, False
                        )
                        geompy.ExportSTL(
                            back, os.path.join(geomdir, "back.stl"), True, res2, False
                        )


# -------------------------------------------------------- #
#                          MERGING                         #
# -------------------------------------------------------- #

import os


def merge_stl_files(file_paths):
    """
    Merge multiple STL files into one.
    Add the name of the file as a label to the 'solid' and 'endsolid' lines.
    """
    merged_content = []

    for file_path in file_paths:
        # Obter o nome do arquivo sem a extensão
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        with open(file_path, "r") as f:
            content = f.readlines()

            # Substituir a linha 'solid' com o nome do arquivo
            content[0] = f"solid {file_name}\n"  # Substituindo a linha 'solid'

            # Substituir a linha 'endsolid' com o nome do arquivo
            for i in range(len(content)):
                if content[i].startswith("endsolid"):
                    content[i] = f"endsolid {file_name}\n"
                    break

            merged_content.extend(content)

    return merged_content


def save_merged_stl(content, output_path):
    """
    Save the merged content to a new STL file.
    """
    with open(output_path, "w") as f:
        f.writelines(content)


def process_and_merge_stls():
    base_directory = "geometries/domain"  # Caminho para a pasta geometries/domain
    merged_directory = "geometries/merged"  # Caminho para a pasta merged

    # Garantir que a pasta merged existe
    os.makedirs(merged_directory, exist_ok=True)

    # Listar as pastas que começam com 'geom'
    geom_folders = [f for f in os.listdir(base_directory) if f.startswith("geom")]

    for folder in geom_folders:
        # Caminho para a pasta 'default' e a pasta 'geomXXX'
        default_folder = os.path.join(base_directory, "default")
        current_folder = os.path.join(base_directory, folder)

        # Listar todos os arquivos .stl nas pastas 'default' e 'geomXXX'
        stl_files = [f for f in os.listdir(default_folder) if f.endswith(".stl")]
        stl_files += [f for f in os.listdir(current_folder) if f.endswith(".stl")]

        # Caminhos completos para os arquivos .stl
        file_paths = [
            os.path.join(default_folder, file)
            for file in stl_files
            if file in os.listdir(default_folder)
        ]
        file_paths += [
            os.path.join(current_folder, file)
            for file in stl_files
            if file in os.listdir(current_folder)
        ]

        # Mesclar os arquivos STL
        merged_content = merge_stl_files(file_paths)

        # Definir o caminho de saída
        output_file = os.path.join(merged_directory, f"{folder}.stl")

        # Salvar o arquivo STL mesclado
        save_merged_stl(merged_content, output_file)
        print(f"Arquivo salvo: {output_file}")


# -------------------------------------------------------- #
#                         EXECUTION                        #
# -------------------------------------------------------- #
semicircle()
ellipsoid()
triangle()
quadrilateral()
combined_shapes()
# ------------------------- merge ------------------------ #
process_and_merge_stls()


# -------------------------------------------------------- #
#                          CLOSING                         #
# -------------------------------------------------------- #

if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()
