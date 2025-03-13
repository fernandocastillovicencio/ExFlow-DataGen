import os
import numpy as np
import pyvista as pv
import pickle


def extract_vtk_data(case_dir, output_dir="processed_data"):
    """
    Extrai os dados brutos do OpenFOAM a partir dos arquivos VTK gerados pelo foamToVTK.

    Args:
        case_dir (str): Diretório do caso OpenFOAM.
        output_dir (str): Diretório onde os arquivos extraídos serão salvos.
    """
    print(f"🔄 Extraindo dados VTK do caso: {case_dir}")

    # 🔹 Encontrar a pasta VTK dentro do caso
    vtk_dir = os.path.join(case_dir, "VTK")
    if not os.path.exists(vtk_dir):
        print(f"❌ Diretório VTK não encontrado para {case_dir}.")
        return False

    # 🔹 Buscar a última pasta de tempo disponível
    subdirs = [
        d for d in os.listdir(vtk_dir) if os.path.isdir(os.path.join(vtk_dir, d))
    ]
    if not subdirs:
        print("❌ Nenhum diretório de tempo encontrado dentro de 'VTK/'.")
        return False

    last_vtk_dir = os.path.join(vtk_dir, sorted(subdirs)[-1])  # Última pasta de tempo

    # 🔹 Ler o arquivo principal de malha interna (internal.vtu)
    vtu_file = os.path.join(last_vtk_dir, "internal.vtu")
    if not os.path.exists(vtu_file):
        print(f"❌ Arquivo {vtu_file} não encontrado.")
        return False

    mesh = pv.read(vtu_file)

    # 🔹 Extrair coordenadas dos pontos
    points = mesh.points  # (N, 3) coordenadas XYZ

    # 🔹 Extrair campos escalares e vetoriais
    if "p" in mesh.point_data:
        p = mesh.point_data["p"]  # Pressão (N,)
    else:
        print("⚠ Campo 'p' não encontrado no VTK.")
        p = np.zeros(len(points))

    if "U" in mesh.point_data:
        U = mesh.point_data["U"]  # Velocidade vetorial (N, 3)
        Ux, Uy = U[:, 0], U[:, 1]  # Somente componentes X e Y
    else:
        print("⚠ Campo 'U' não encontrado no VTK.")
        Ux, Uy = np.zeros(len(points)), np.zeros(len(points))

    # 🔹 Criar diretório de saída e garantir que ele existe
    os.makedirs(output_dir, exist_ok=True)

    # 🔹 Salvar os arquivos no formato NumPy
    np.save(os.path.join(output_dir, "points.npy"), points)
    np.save(os.path.join(output_dir, "Ux.npy"), Ux)
    np.save(os.path.join(output_dir, "Uy.npy"), Uy)
    np.save(os.path.join(output_dir, "p.npy"), p)

    # 🔹 Salvar também no formato `.pkl` para compatibilidade com outros scripts
    data_dict = {"points": points, "Ux": Ux, "Uy": Uy, "p": p}
    with open(os.path.join(output_dir, "raw_data.pkl"), "wb") as f:
        pickle.dump(data_dict, f)

    print(f"✅ Dados extraídos e salvos em {output_dir}")
    return True
