import os
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from shapely.geometry import Polygon, Point  # Corrigindo a importação de Point

def list_cases(cases_dir, max_cases=None):
    """Lista as pastas de casos dentro do diretório `cases_dir`."""
    cases = sorted([os.path.join(cases_dir, case) for case in os.listdir(cases_dir) if os.path.isdir(os.path.join(cases_dir, case))])
    return cases[:max_cases] if max_cases else cases

def run_foamToVTK(case_path):
    """Executa o comando foamToVTK no caso especificado."""
    os.system(f"cd {case_path} && foamToVTK -latestTime")
    print(f"✅ foamToVTK executado para {case_path}")

def load_vtu_data(vtu_file):
    """Carrega o arquivo VTU e extrai as variáveis relevantes."""
    mesh = pv.read(vtu_file)
    coordinates = mesh.points[:, :2]
    p = mesh.point_data['p']
    Ux = mesh.point_data['U'][:, 0]
    Uy = mesh.point_data['U'][:, 1]
    return coordinates, p, Ux, Uy

def create_fixed_grid(coordinates, grid_width=172, grid_height=79):
    """Cria uma grade fixa 172x79 baseada nos limites do domínio."""
    x_min, y_min = np.min(coordinates, axis=0)
    x_max, y_max = np.max(coordinates, axis=0)
    return np.meshgrid(np.linspace(x_min, x_max, grid_width), np.linspace(y_min, y_max, grid_height))

def interpolate_data(coordinates, field_data, grid_x, grid_y):
    """Interpola os dados do campo para a grade fixa."""
    return np.nan_to_num(griddata(coordinates, field_data, (grid_x, grid_y), method='cubic'))

def apply_obstacle_mask(p, Ux, Uy, grid_x, grid_y, obstacle_polygon):
    """Zera os valores dentro do obstáculo detectado."""
    grid_shape = grid_x.shape
    mask = np.zeros(grid_shape, dtype=bool)

    for i in range(grid_shape[0]):  
        for j in range(grid_shape[1]):  
            point = Point(grid_x[i, j], grid_y[i, j])  # Correção: Usando Point corretamente
            if obstacle_polygon.contains(point):
                mask[i, j] = True  

    p[mask] = 0
    Ux[mask] = 0
    Uy[mask] = 0
    return p, Ux, Uy

def save_npy(post_case_dir, grid_x, grid_y, p, Ux, Uy):
    """Salva os dados em post*/data/."""
    data_dir = os.path.join(post_case_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    npy_file = os.path.join(data_dir, "processed_data.npy")
    np.save(npy_file, {'x': grid_x, 'y': grid_y, 'p': p, 'Ux': Ux, 'Uy': Uy})
    print(f"✅ Dados salvos no arquivo: {npy_file}")

def save_image(post_case_dir, grid_x, grid_y, field_data, field_name):
    """Salva imagens em post*/data/figures/."""
    figures_dir = os.path.join(post_case_dir, "data", "figures")
    os.makedirs(figures_dir, exist_ok=True)

    plot_filename = os.path.join(figures_dir, f'{field_name}_172x79_from_npy.png')
    
    plt.figure(figsize=(8, 4))
    plt.contourf(grid_x, grid_y, field_data, levels=100, cmap='jet')
    plt.colorbar(label=field_name)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Campo {field_name}')
    plt.savefig(plot_filename, dpi=300)
    plt.close()
    print(f"✅ Imagem salva em: {plot_filename}")

def prepare_post_dir(case):
    """Prepara o diretório para o pós-processamento, criando os links simbólicos para VTK."""
    # Definir o diretório de pós-processamento
    post_case_dir = os.path.join("postprocesses", f"post_{os.path.basename(case)}")
    
    # Cria o diretório principal de pós-processamento
    os.makedirs(post_case_dir, exist_ok=True)
    print(f"📂 Diretório de pós-processamento configurado: {post_case_dir}")

    # Criar link simbólico para a pasta VTK
    vtk_source = os.path.join(case, "VTK")
    vtk_target = os.path.join(post_case_dir, "VTK")
    
    if os.path.exists(vtk_target) or os.path.islink(vtk_target):
        os.unlink(vtk_target)  # Remove qualquer link simbólico ou diretório existente
    
    os.symlink(os.path.abspath(vtk_source), vtk_target)  # Cria o link simbólico
    print(f"🔗 Link simbólico criado: {vtk_target} -> {vtk_source}")
