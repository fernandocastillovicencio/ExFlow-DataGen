import os
import numpy as np
import pandas as pd
import h5py
from postprocess.config import OUTPUT_DIR, HDF5_FILE_NAME, VELOCITIES

def find_case_by_velocity(velocity):
    """Encontra o diretório do caso correspondente a uma velocidade específica."""
    case_name = f"U{str(velocity).replace('.', '')}"  # Ex: 1.3 → "U13"
    case_dir = os.path.join(OUTPUT_DIR, case_name)

    if os.path.exists(case_dir):
        return case_dir
    else:
        print(f"⚠️ Aviso: Não foi encontrado um caso para Uref={velocity} m/s.")
        return None

def combine_hdf5():
    """Combina os dados de todos os casos HDF5 em um único arquivo, garantindo que cada velocidade seja processada corretamente."""
    all_data = []

    for velocity in VELOCITIES:
        case_dir = find_case_by_velocity(velocity)
        if case_dir is None:
            continue  # Se o diretório não existe, ignora essa velocidade

        hdf5_path = os.path.join(case_dir, HDF5_FILE_NAME)
        if not os.path.exists(hdf5_path):
            print(f"❌ Arquivo HDF5 não encontrado em {case_dir}, pulando...")
            continue

        # Abrir o arquivo HDF5 e ler os dados
        with h5py.File(hdf5_path, "r") as f:
            data = np.array(f["data"])
            column_names = f.attrs["column_names"].split(",")  # ["x", "y", "p", "Ux", "Uy"]

        # Criar um DataFrame e adicionar a coluna Uref
        df = pd.DataFrame(data, columns=column_names)
        df.insert(0, "Uref", velocity)  # Adicionar Uref na primeira coluna

        all_data.append(df)

    if not all_data:
        print("❌ Nenhum dado foi encontrado para combinar.")
        return

    # Concatenar todos os DataFrames
    final_df = pd.concat(all_data, ignore_index=True)

    # Salvar o DataFrame único
    output_path = os.path.join(OUTPUT_DIR, "all_data.h5")
    final_df.to_hdf(output_path, key="dataset", mode="w")

    print(f"✅ Dados combinados salvos em {output_path} ({len(final_df)} linhas)")

def main():
    """Executa a combinação dos dados HDF5."""
    combine_hdf5()
