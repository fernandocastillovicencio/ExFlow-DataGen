from scipy.spatial import cKDTree
import numpy as np


def compute_SDF(points, grid_x, grid_y):
    """
    Calcula a Signed Distance Function (SDF1) de acordo com o artigo de Ribeiro.

    - SDF < 0 dentro do obstáculo.
    - SDF = 0 na superfície do obstáculo (wall).
    - SDF > 0 fora do obstáculo, crescendo suavemente até os limites externos (inlet, outlet, top, bottom).

    Args:
        points (array): Coordenadas X, Y do obstáculo.
        grid_x (array): Coordenadas X da malha estruturada.
        grid_y (array): Coordenadas Y da malha estruturada.

    Returns:
        array: Matriz SDF corrigida de tamanho (172, 79).
    """
    X, Y = np.meshgrid(grid_x, grid_y, indexing="ij")  # Criar grade estruturada

    # Criar KDTree com os pontos da superfície do obstáculo
    tree_obstacle = cKDTree(points)

    # Calcular distância para o obstáculo
    sdf = tree_obstacle.query(np.c_[X.ravel(), Y.ravel()])[0]
    sdf = sdf.reshape(len(grid_x), len(grid_y))  # Ajustar formato

    # Identificar pontos dentro do obstáculo (Raio de tolerância: 1e-3)
    inside_mask = tree_obstacle.query_ball_point(np.c_[X.ravel(), Y.ravel()], 1e-3)
    inside_mask = np.array([len(pts) > 0 for pts in inside_mask]).reshape(sdf.shape)

    # Aplicar regras do SDF conforme Ribeiro
    sdf[inside_mask] *= -1  # Dentro do obstáculo, SDF deve ser negativo

    # ========================================================== #
    #         Ajuste para distâncias às paredes externas         #
    # ========================================================== #

    # Criar árvores KDTree para os limites externos (INLET, OUTLET, TOP, BOTTOM)
    boundary_points = []

    # Inlet (x mínimo)
    for y in grid_y:
        boundary_points.append([-0.060, y])

    # Outlet (x máximo)
    for y in grid_y:
        boundary_points.append([0.200, y])

    # Top (y máximo)
    for x in grid_x:
        boundary_points.append([x, 0.060])

    # Bottom (y mínimo)
    for x in grid_x:
        boundary_points.append([x, -0.060])

    # Converter em array e criar KDTree para os limites
    boundary_points = np.array(boundary_points)
    tree_boundary = cKDTree(boundary_points)

    # Calcular distância de cada ponto até o limite externo mais próximo
    sdf_boundary = tree_boundary.query(np.c_[X.ravel(), Y.ravel()])[0]
    sdf_boundary = sdf_boundary.reshape(len(grid_x), len(grid_y))

    # Atualizar SDF para crescer até as bordas externas
    sdf_outside = np.where(sdf > 0, sdf + sdf_boundary, sdf)

    return sdf_outside


def compute_flow_region(sdf):
    """
    Gera a matriz de flow region channel conforme o artigo de Ribeiro.

    Args:
        sdf (array): Matriz SDF corrigida.

    Returns:
        array: Flow region channel.
    """
    if sdf.shape != (172, 79):
        raise ValueError(f"Erro: sdf tem formato {sdf.shape}, esperado (172, 79)")

    flow_region = np.ones((172, 79))
    flow_region[sdf < 0] = 0  # Dentro do obstáculo
    flow_region[0, :] = 3  # Entrada (inlet)
    flow_region[-1, :] = 4  # Saída (outlet)
    flow_region[:, 0] = 2  # Freestream lateral
    flow_region[:, -1] = 2  # Freestream lateral

    return flow_region
