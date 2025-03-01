import os
import numpy as np
import pickle
from modules.postprocessing.convert_to_vtk import convert_to_vtk
from modules.postprocessing.extract_fields import extract_fields
from modules.postprocessing.interpolate_fields import interpolate_fields
from modules.postprocessing.generate_dataX import compute_SDF, compute_flow_region


def process_all_cases(cases_dir, output_dir="processed_data"):
    """
    Processa todas as pastas de simulação e gera arquivos intermediários `.npy` dentro da pasta `processed/`.
    Depois, consolida tudo em `processed_data/`.

    Args:
        cases_dir (str): Diretório contendo os casos.
        output_dir (str): Diretório onde os arquivos finais serão armazenados.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Criar diretório central se não existir

    cases = [
        os.path.join(cases_dir, d)
        for d in os.listdir(cases_dir)
        if d.startswith("case")
    ]

    # Criar grade global para interpolação
    grid_x = np.linspace(-0.060, 0.200, 172)
    grid_y = np.linspace(-0.060, 0.060, 79)

    print(f"🔄 Iniciando pós-processamento para {len(cases)} casos...")

    for case in cases:
        vtk_folder = convert_to_vtk(case)
        if vtk_folder:
            points, Ux, Uy, p = extract_fields(vtk_folder)
            Ux_grid, Uy_grid, p_grid = interpolate_fields(
                points, Ux, Uy, p, grid_x, grid_y
            )
            sdf1 = compute_SDF(points, grid_x, grid_y)
            flow_region = compute_flow_region(sdf1)

            # Criar pasta `processed/` dentro do caso
            processed_dir = os.path.join(case, "processed")
            if not os.path.exists(processed_dir):
                os.makedirs(processed_dir)

            # Salvar arquivos intermediários em `.npy` dentro de `processed/`
            np.save(
                os.path.join(processed_dir, "dataY.npy"),
                np.stack([Ux_grid, Uy_grid, p_grid], axis=0),
            )
            np.save(
                os.path.join(processed_dir, "dataX.npy"),
                np.stack([sdf1, flow_region, sdf1], axis=0),
            )

    print("✅ Todos os arquivos intermediários foram gerados.")
    merge_processed_data(cases, output_dir)


def merge_processed_data(cases, output_dir):
    """
    Consolida os arquivos individuais e salva `dataX.pkl` e `dataY.pkl` corretamente.

    Args:
        cases (list): Lista de diretórios de cada caso processado.
        output_dir (str): Diretório onde os arquivos finais serão armazenados.
    """
    dataX_list = []
    dataY_list = []

    for case in cases:
        processed_dir = os.path.join(case, "processed")
        dataX_path = os.path.join(processed_dir, "dataX.npy")
        dataY_path = os.path.join(processed_dir, "dataY.npy")

        if os.path.exists(dataX_path) and os.path.exists(dataY_path):
            x = np.load(dataX_path)  # Esperado (1,3,172,79)
            y = np.load(dataY_path)  # Esperado (1,3,172,79)

            if x.shape != (1, 3, 172, 79) or y.shape != (1, 3, 172, 79):
                print(
                    f"⚠️ Dimensão inesperada em {case}: {x.shape}, {y.shape}. Ignorando..."
                )
                continue

            dataX_list.append(x)  # Mantemos (1,3,172,79)
            dataY_list.append(y)

        else:
            print(f"⚠ Arquivo ausente em {case}, pulando...")

    if dataX_list and dataY_list:
        dataX_final = np.concatenate(dataX_list, axis=0)  # (N,3,172,79)
        dataY_final = np.concatenate(dataY_list, axis=0)  # (N,3,172,79)

        # Verificação antes de salvar
        if dataX_final.shape[1:] != (3, 172, 79) or dataY_final.shape[1:] != (
            3,
            172,
            79,
        ):
            print(
                f"❌ ERRO: Formato incorreto após concatenação: dataX {dataX_final.shape}, dataY {dataY_final.shape}"
            )
            return

        with open(os.path.join(output_dir, "dataX.pkl"), "wb") as f:
            pickle.dump(dataX_final, f)
        with open(os.path.join(output_dir, "dataY.pkl"), "wb") as f:
            pickle.dump(dataY_final, f)

        print(f"✅ Arquivos consolidados salvos em '{output_dir}/'")

    else:
        print("❌ Nenhum dado válido encontrado para consolidar!")


if __name__ == "__main__":
    process_all_cases("cases/")
