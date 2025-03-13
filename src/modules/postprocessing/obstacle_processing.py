import pyvista as pv
import numpy as np
from shapely.geometry import Polygon, Point

def load_wall_vtp(wall_vtp_file):
    """Carrega o arquivo VTP de parede e extrai as coordenadas da superfície."""
    wall_mesh = pv.read(wall_vtp_file)
    return wall_mesh.points[:, :2]  # Coordenadas da superfície da parede

def cartesian_to_cylindrical(x, y):
    """Converte coordenadas cartesianas para cilíndricas (r, theta)."""
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, theta

def sort_points_by_theta(wall_coordinates):
    """Ordena os pontos com base no ângulo theta em coordenadas cilíndricas, no sentido anti-horário."""
    r, theta = cartesian_to_cylindrical(wall_coordinates[:, 0], wall_coordinates[:, 1])
    sorted_indices = np.argsort(theta)
    return wall_coordinates[sorted_indices]

def create_polygon_from_sorted_points(sorted_coordinates):
    """Cria um polígono a partir dos pontos ordenados em sentido anti-horário."""
    sorted_coordinates = np.vstack([sorted_coordinates, sorted_coordinates[0]])  # Fechar o polígono
    return Polygon(sorted_coordinates)

def get_obstacle_polygon(wall_vtp_file):
    """Obtém o polígono do obstáculo a partir do arquivo wall.vtp."""
    wall_coordinates = load_wall_vtp(wall_vtp_file)
    sorted_coordinates = sort_points_by_theta(wall_coordinates)
    return create_polygon_from_sorted_points(sorted_coordinates)

def apply_obstacle_mask(p, Ux, Uy, grid_x, grid_y, obstacle_polygon):
    """Substitui os valores dentro do obstáculo por zero na grade 2D."""
    grid_shape = grid_x.shape
    mask = np.zeros(grid_shape, dtype=bool)

    for i in range(grid_shape[0]):  
        for j in range(grid_shape[1]):  
            point = Point(grid_x[i, j], grid_y[i, j])
            if obstacle_polygon.contains(point):
                mask[i, j] = True  

    p[mask] = 0
    Ux[mask] = 0
    Uy[mask] = 0
    return p, Ux, Uy
