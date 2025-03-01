import os
import numpy as np
import pickle


import os
import numpy as np
import pickle


def merge_processed_data(cases_dir, output_dir="processed_data"):
    """
    Consolida os arquivos `.npy` de cada caso e gera `dataX.pkl` e `dataY.pkl`.

    Args:
        cases_dir (str): Diretório contendo os casos processados.
        output_dir (str): Diretório onde os arquivos finais serão armazenados.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dataX_list = []
    dataY_list = []

    cases = [
        os.path.join(cases_dir, d)
        for d in os.listdir(cases_dir)
        if d.startswith("case")
    ]

    print(f"🔄 Iniciando junção dos arquivos de {len(cases)} casos...")

    for case in cases:
        processed_dir = os.path.join(case, "processed")
        dataX_path = os.path.join(processed_dir, "dataX.npy")
        dataY_path = os.path.join(processed_dir, "dataY.npy")

        if os.path.exists(dataX_path) and os.path.exists(dataY_path):
            x = np.load(dataX_path)  # (3,172,79)
            y = np.load(dataY_path)  # (3,172,79)

            # 🔥 Aqui adicionamos a dimensão correta (1,3,172,79)
            x = np.expand_dims(x, axis=0)  # (1,3,172,79)
            y = np.expand_dims(y, axis=0)  # (1,3,172,79)

            dataX_list.append(x)
            dataY_list.append(y)
        else:
            print(f"⚠ Arquivo ausente em {case}, pulando...")

    if dataX_list and dataY_list:
        dataX_final = np.concatenate(dataX_list, axis=0)  # (N,3,172,79)
        dataY_final = np.concatenate(dataY_list, axis=0)  # (N,3,172,79)

        with open(os.path.join(output_dir, "dataX.pkl"), "wb") as f:
            pickle.dump(dataX_final, f)
        with open(os.path.join(output_dir, "dataY.pkl"), "wb") as f:
            pickle.dump(dataY_final, f)

        print(f"✅ Arquivos consolidados salvos em '{output_dir}/'")

    else:
        print("❌ Nenhum dado válido encontrado para consolidar!")


if __name__ == "__main__":
    merge_processed_data("cases/")
