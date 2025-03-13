import os
import numpy as np
# Import das funções gerais
from modules.postprocessing.postprocess_utils import list_cases

# Import das funções para gerar Y
from modules.postprocessing.postprocess_utils import (
    run_foamToVTK, load_vtu_data, create_fixed_grid,
    interpolate_data, apply_obstacle_mask, save_npy, save_image
)
from modules.postprocessing.obstacle_processing import get_obstacle_polygon

# Import das funções para gerar X
from modules.postprocessing.sdf1_generation import generate_sdf1, save_sdf1_image
from modules.postprocessing.flow_region_generation import generate_flow_region, save_flow_region_image
from modules.postprocessing.sdf2_generation import generate_sdf2, save_sdf2_image

def prepare_case_directory(case):
    """Cria o diretório de pós-processamento e o link simbólico para a pasta VTK"""
    post_case_dir = os.path.join("postprocesses", f"{os.path.basename(case)}")
    os.makedirs(post_case_dir, exist_ok=True)
    print(f"📂 Diretório de pós-processamento configurado: {post_case_dir}")

    vtk_source = os.path.join(case, "VTK")
    vtk_target = os.path.join(post_case_dir, "VTK")

    if os.path.exists(vtk_target) or os.path.islink(vtk_target):
        os.unlink(vtk_target)
    
    os.symlink(os.path.abspath(vtk_source), vtk_target)
    print(f"🔗 Link simbólico criado: {vtk_target} -> {vtk_source}")
    
    return post_case_dir


def process_fields(case, post_case_dir):
    """Processa os dados do arquivo VTU, cria a grade e faz a interpolação"""
    vtk_source = os.path.join(case, "VTK")
    vtk_file = os.path.join(vtk_source, f"{os.path.basename(case)}_500", "internal.vtu")
    print(f"📂 Carregando arquivo VTU: {vtk_file}")
    coordinates, p, Ux, Uy = load_vtu_data(vtk_file)

    grid_x, grid_y = create_fixed_grid(coordinates)
    p_interpolated = interpolate_data(coordinates, p, grid_x, grid_y)
    Ux_interpolated = interpolate_data(coordinates, Ux, grid_x, grid_y)
    Uy_interpolated = interpolate_data(coordinates, Uy, grid_x, grid_y)

    return p_interpolated, Ux_interpolated, Uy_interpolated, grid_x, grid_y


def apply_obstacle(case, p_interpolated, Ux_interpolated, Uy_interpolated, grid_x, grid_y):
    """Aplica a máscara do obstáculo aos dados interpolados"""
    wall_vtp_file = os.path.join(case, "VTK", f"{os.path.basename(case)}_500", "boundary", "wall.vtp")
    print(f"📂 Carregando obstáculo do arquivo: {wall_vtp_file}")
    obstacle_polygon = get_obstacle_polygon(wall_vtp_file)
    p_interpolated, Ux_interpolated, Uy_interpolated = apply_obstacle_mask(
        p_interpolated, Ux_interpolated, Uy_interpolated, grid_x, grid_y, obstacle_polygon
    )

    return p_interpolated, Ux_interpolated, Uy_interpolated


def save_results(post_case_dir, grid_x, grid_y, p_interpolated, Ux_interpolated, Uy_interpolated):
    """Salva os resultados em .npy e imagens .png"""
    print(f"📂 Salvando dados e imagens para o caso: {post_case_dir}")
    save_npy(post_case_dir, grid_x, grid_y, p_interpolated, Ux_interpolated, Uy_interpolated)
    save_image(post_case_dir, grid_x, grid_y, p_interpolated, "Pressure")
    save_image(post_case_dir, grid_x, grid_y, Ux_interpolated, "Velocity_X")
    save_image(post_case_dir, grid_x, grid_y, Uy_interpolated, "Velocity_Y")




def save_Ydata(case, post_case_dir):
    # Step 2.2: Process the fields (VTU data, grid creation, interpolation)
    p_interpolated, Ux_interpolated, Uy_interpolated, grid_x, grid_y = process_fields(case, post_case_dir)

    # Step 2.3: Apply obstacle mask
    p_corrected, Ux_corrected, Uy_corrected = apply_obstacle(case, p_interpolated, Ux_interpolated, Uy_interpolated, grid_x, grid_y)

    # Step 2.4: Save results (npy and images)
    save_results(post_case_dir, grid_x, grid_y, p_corrected, Ux_corrected, Uy_corrected)

def save_Xdata(case, post_case_dir):
    """
    Gera e salva as três variáveis de entrada (SDF1, flow_region e SDF2).
    """
    # 1) Definir caminhos relevantes
    vtu_file = os.path.join(case, "VTK", f"{os.path.basename(case)}_500", "internal.vtu")
    obstacle_file = os.path.join(case, "VTK", f"{os.path.basename(case)}_500", "boundary", "wall.vtp")

    # Diretórios corretos para salvar os arquivos
    data_dir = os.path.join(post_case_dir, "data")
    figures_dir = os.path.join(data_dir, "figures")

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    # 2) Gerar SDF1
    sdf1 = generate_sdf1(vtu_file, obstacle_file)
    save_sdf1_image(sdf1, figures_dir)

    # 3) Gerar flow_region
    flow_region = generate_flow_region(vtu_file, obstacle_file)
    save_flow_region_image(flow_region, figures_dir)

    # 4) Gerar SDF2
    sdf2 = generate_sdf2(vtu_file)
    save_sdf2_image(sdf2, figures_dir)

    # 5) Salvar os dados no arquivo .npy
    output_file = os.path.join(data_dir, "dataX.npy")
    np.save(output_file, {"sdf1": sdf1, "flow_region": flow_region, "sdf2": sdf2})

    print(f"✅ Arquivo dataX.npy salvo em: {output_file}")
    print(f"✅ Imagens salvas em: {figures_dir}")


def postprocessing_control():
    cases_dir = os.path.join(os.getcwd(), "cases")
    print(f"📂 Iniciando o pós-processamento no diretório: {cases_dir}")

    # Step 1: List cases
    cases = list_cases(cases_dir, max_cases=2)
    print(f"🔍 Casos listados: {cases}")

    # Step 2: Process each case
    for case in cases:
        print(f"⚙ Preparando diretórios e processando o caso: {case}")

        # Step 2.1: Prepare directory and symbolic link for VTK
        post_case_dir = prepare_case_directory(case)


        # Step 2.2: Save Y-data
        save_Ydata(case, post_case_dir)

        # Step 2.3: Save X-data
        save_Xdata(case, post_case_dir)
        
        # Step 2.4: Save overall data





if __name__ == "__main__":
    postprocessing_control()
