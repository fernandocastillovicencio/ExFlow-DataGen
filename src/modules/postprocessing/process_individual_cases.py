import os
import numpy as np
import multiprocessing
from modules.postprocessing.convert_to_vtk import convert_to_vtk
from modules.postprocessing.extract_fields import extract_fields
from modules.postprocessing.interpolate_fields import interpolate_fields
from modules.postprocessing.generate_dataX import compute_SDF, compute_flow_region


def process_case(case):
    """
    Processa um único caso e salva os arquivos intermediários `.npy` na pasta `processed/`.

    Args:
        case (str): Caminho para a pasta do caso.
    """
    vtk_folder = convert_to_vtk(case)
    if vtk_folder:
        # Criar pasta `processed/`
        processed_dir = os.path.join(case, "processed")
        os.makedirs(processed_dir, exist_ok=True)

        # Definir grade
        grid_x = np.linspace(-0.060, 0.200, 172)
        grid_y = np.linspace(-0.060, 0.060, 79)

        # Extrair e processar os dados
        points, Ux, Uy, p = extract_fields(vtk_folder)
        Ux_grid, Uy_grid, p_grid = interpolate_fields(points, Ux, Uy, p, grid_x, grid_y)
        sdf1 = compute_SDF(points, grid_x, grid_y)
        flow_region = compute_flow_region(sdf1)

        # Salvar os arquivos `.npy`
        np.save(
            os.path.join(processed_dir, "dataY.npy"),
            np.stack([Ux_grid, Uy_grid, p_grid], axis=0),
        )
        np.save(
            os.path.join(processed_dir, "dataX.npy"),
            np.stack([sdf1, flow_region, sdf1], axis=0),
        )

        print(f"✅ Processamento concluído para {case}")


def process_all_cases_parallel(cases_dir, num_workers=4):
    """
    Processa todas as pastas `case_*` em paralelo.

    Args:
        cases_dir (str): Diretório contendo os casos.
        num_workers (int): Número de processos em paralelo.
    """
    cases = [
        os.path.join(cases_dir, d)
        for d in os.listdir(cases_dir)
        if d.startswith("case")
    ]

    print(f"🔄 Iniciando processamento paralelo para {len(cases)} casos...")

    with multiprocessing.Pool(num_workers) as pool:
        pool.map(process_case, cases)

    print(
        "✅ Todos os casos foram processados e arquivos intermediários foram gerados!"
    )


if __name__ == "__main__":
    process_all_cases_parallel(
        "cases/", num_workers=8
    )  # Definir número de núcleos da CPU
