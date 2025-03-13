import os
import numpy as np
import pickle
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
    
    # Criar diretório "figures" antes de salvar imagens
    figures_dir = os.path.join(post_case_dir, "data", "figures")
    os.makedirs(figures_dir, exist_ok=True)  # 🔹 GARANTIR QUE O DIRETÓRIO EXISTA

    print(f"📂 Salvando dados e imagens para o caso: {post_case_dir}")

    # Salvar os dados interpolados em .npy
    save_npy(post_case_dir, grid_x, grid_y, p_interpolated, Ux_interpolated, Uy_interpolated)

    # Salvar imagens
    save_image(post_case_dir, grid_x, grid_y, p_interpolated, "Pressure")
    save_image(post_case_dir, grid_x, grid_y, Ux_interpolated, "Velocity_X")
    save_image(post_case_dir, grid_x, grid_y, Uy_interpolated, "Velocity_Y")

    print(f"✅ Todas as imagens foram salvas em {figures_dir}")





def save_Ydata(case, post_case_dir):
    """
    Gera e salva os dados de saída (P, Ux, Uy) no formato adequado para a rede neural.
    """
    # Criar o diretório "data" se ele não existir antes de salvar os arquivos
    data_dir = os.path.join(post_case_dir, "data")
    os.makedirs(data_dir, exist_ok=True)  # 🔹 GARANTIR QUE O DIRETÓRIO EXISTA

    # Processar campos (VTU data, grid, interpolação)
    p_interpolated, Ux_interpolated, Uy_interpolated, grid_x, grid_y = process_fields(case, post_case_dir)

    # Aplicar máscara do obstáculo
    p_corrected, Ux_corrected, Uy_corrected = apply_obstacle(case, p_interpolated, Ux_interpolated, Uy_interpolated, grid_x, grid_y)

    # Reformatar para o formato (1, 3, 172, 79)
    Y_data = np.stack([p_corrected, Ux_corrected, Uy_corrected], axis=0)  # Forma (3, 172, 79)
    Y_data = np.expand_dims(Y_data, axis=0)  # Forma final (1, 3, 172, 79)

    # Salvar em dataY.npy
    output_file = os.path.join(data_dir, "dataY.npy")
    np.save(output_file, Y_data)

    print(f"✅ Arquivo dataY.npy salvo em: {output_file} com formato {Y_data.shape}")

    # Salvar as imagens de p, Ux, Uy
    figures_dir = os.path.join(data_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    save_image(post_case_dir, grid_x, grid_y, p_corrected, "Pressure")
    save_image(post_case_dir, grid_x, grid_y, Ux_corrected, "Velocity_X")
    save_image(post_case_dir, grid_x, grid_y, Uy_corrected, "Velocity_Y")




def save_Xdata(case, post_case_dir):
    """
    Gera e salva as três variáveis de entrada (SDF1, flow_region e SDF2) no formato adequado para a rede neural.
    """
    # Criar o diretório "data" se ele não existir antes de salvar os arquivos
    data_dir = os.path.join(post_case_dir, "data")
    figures_dir = os.path.join(data_dir, "figures")
    os.makedirs(data_dir, exist_ok=True)  # 🔹 GARANTIR QUE O DIRETÓRIO EXISTA

    # 1) Definir caminhos relevantes
    vtu_file = os.path.join(case, "VTK", f"{os.path.basename(case)}_500", "internal.vtu")
    obstacle_file = os.path.join(case, "VTK", f"{os.path.basename(case)}_500", "boundary", "wall.vtp")

    # 2) Gerar SDF1, Flow Region e SDF2
    sdf1 = generate_sdf1(vtu_file, obstacle_file)
    flow_region = generate_flow_region(vtu_file, obstacle_file)
    sdf2 = generate_sdf2(vtu_file)

    # 3) Reformatar para o formato (1, 3, 172, 79)
    X_data = np.stack([sdf1, flow_region, sdf2], axis=0)  # Forma (3, 172, 79)
    X_data = np.expand_dims(X_data, axis=0)  # Forma final (1, 3, 172, 79)

    # 4) Salvar em dataX.npy
    output_file = os.path.join(data_dir, "dataX.npy")
    np.save(output_file, X_data)

    # Salvar imagens
    save_sdf1_image(sdf1, figures_dir)
    save_flow_region_image(flow_region, figures_dir)
    save_sdf2_image(sdf2, figures_dir)

    print(f"✅ Arquivo dataX.npy salvo em: {output_file} com formato {X_data.shape}")


def save_overall_data(cases):
    """
    Lê os arquivos dataX.npy e dataY.npy de cada pasta de caso,
    empilha (concatena) ao longo da dimensão 0,
    e salva dataX.pkl e dataY.pkl no diretório postprocesses/processed_data com dimensões (N, 3, 172, 79).
    """
    dataX_list = []
    dataY_list = []

    for case in cases:
        # post_case_dir corresponde a postprocesses/<nome_da_pasta>
        post_case_dir = os.path.join("postprocesses", os.path.basename(case))
        data_dir = os.path.join(post_case_dir, "data")

        # Arquivos gerados anteriormente
        fileX = os.path.join(data_dir, "dataX.npy")
        fileY = os.path.join(data_dir, "dataY.npy")

        # Ler cada arquivo .npy
        if os.path.exists(fileX):
            x_data = np.load(fileX)  # (1,3,172,79)
            dataX_list.append(x_data)
        
        if os.path.exists(fileY):
            y_data = np.load(fileY)  # (1,3,172,79)
            dataY_list.append(y_data)

    # Concatenar ao longo de axis=0
    # Se tivermos N pastas, resultará em (N,3,172,79)
    if dataX_list:
        dataX_all = np.concatenate(dataX_list, axis=0)
    else:
        dataX_all = None

    if dataY_list:
        dataY_all = np.concatenate(dataY_list, axis=0)
    else:
        dataY_all = None

    # Criar a pasta postprocesses/processed_data/ caso não exista
    processed_data_dir = os.path.join("postprocesses", "processed_data")
    os.makedirs(processed_data_dir, exist_ok=True)  # 🔹 GARANTIR QUE A PASTA EXISTA

    # Salvar em arquivos .pkl (poderia ser .npy se preferir)
    if dataX_all is not None:
        with open(os.path.join(processed_data_dir, "dataX.pkl"), "wb") as f:
            pickle.dump(dataX_all, f)
        print(f"✅ Arquivo dataX.pkl salvo em: {os.path.join(processed_data_dir, 'dataX.pkl')} com dimensão {dataX_all.shape}")

    if dataY_all is not None:
        with open(os.path.join(processed_data_dir, "dataY.pkl"), "wb") as f:
            pickle.dump(dataY_all, f)
        print(f"✅ Arquivo dataY.pkl salvo em: {os.path.join(processed_data_dir, 'dataY.pkl')} com dimensão {dataY_all.shape}")



import multiprocessing

def process_single_case(case):
    """Processa um único caso: cria as pastas, processa os dados e salva os resultados."""
    print(f"🔄 Verificando e rodando foamToVTK para o caso: {case}")
    run_foamToVTK(case)  # Executa foamToVTK para cada caso

    print(f"⚙ Preparando diretórios e processando o caso: {case}")

    # Passo 1: Preparar diretório e link simbólico para VTK
    post_case_dir = prepare_case_directory(case)

    # Passo 2: Salvar dados Y e X
    save_Ydata(case, post_case_dir)
    save_Xdata(case, post_case_dir)

    print(f"✅ Processamento do caso {case} concluído.")

def postprocessing_control():
    cases_dir = os.path.join(os.getcwd(), "cases")
    print(f"📂 Iniciando o pós-processamento no diretório: {cases_dir}")

    # Criar a pasta principal de pós-processamento antes de tudo
    postprocesses_dir = os.path.join(os.getcwd(), "postprocesses")
    os.makedirs(postprocesses_dir, exist_ok=True)

    # Criar a pasta processed_data dentro de postprocesses/
    processed_data_dir = os.path.join(postprocesses_dir, "processed_data")
    os.makedirs(processed_data_dir, exist_ok=True)

    print(f"📁 Pastas 'postprocesses/' e 'postprocesses/processed_data/' criadas ou já existentes.")

    # Passo 1: Listar os casos
    cases = list_cases(cases_dir)
    print(f"🔍 {len(cases)} casos encontrados para processamento.")

    # Passo 2: Rodar foamToVTK se necessário e preparar os casos em paralelo
    print(f"🚀 Iniciando processamento paralelo para {len(cases)} casos...")
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(process_single_case, cases)  # Processa todos os casos em paralelo

    # Passo 3: Salvar os dados gerais (concatenar todos os casos)
    save_overall_data(cases)






if __name__ == "__main__":
    postprocessing_control()
