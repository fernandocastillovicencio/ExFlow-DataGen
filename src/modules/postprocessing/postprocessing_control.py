import os
from modules.postprocessing.postprocess_utils import (
    list_cases, run_foamToVTK, load_vtu_data,
    create_fixed_grid, interpolate_data, apply_obstacle_mask, save_npy, save_image
)
from modules.postprocessing.obstacle_processing import get_obstacle_polygon

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

        # Step 2.2: Process the fields (VTU data, grid creation, interpolation)
        p_interpolated, Ux_interpolated, Uy_interpolated, grid_x, grid_y = process_fields(case, post_case_dir)

        # Step 2.3: Apply obstacle mask
        p_interpolated, Ux_interpolated, Uy_interpolated = apply_obstacle(case, p_interpolated, Ux_interpolated, Uy_interpolated, grid_x, grid_y)

        # Step 2.4: Save results (npy and images)
        save_results(post_case_dir, grid_x, grid_y, p_interpolated, Ux_interpolated, Uy_interpolated)


if __name__ == "__main__":
    postprocessing_control()
