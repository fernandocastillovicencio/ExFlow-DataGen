import os
import shutil
import subprocess


def convert_to_vtk(case_dir):
    """
    Remove a pasta VTK (se existir), executa foamToVTK -latestTime e encontra a pasta correta com internal.vtu.

    Args:
        case_dir (str): Caminho da pasta do caso.

    Returns:
        str: Caminho da pasta correta dentro de VTK.
    """
    vtk_path = os.path.join(case_dir, "VTK")

    # 1) Remover a pasta VTK se existir
    if os.path.exists(vtk_path):
        shutil.rmtree(vtk_path)
        print(f"🧹 Pasta VTK removida em {case_dir}")

    # 2) Executar foamToVTK -latestTime
    try:
        subprocess.run("foamToVTK -latestTime", shell=True, check=True, cwd=case_dir)
        print(f"✅ foamToVTK executado com sucesso em {case_dir}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao executar foamToVTK em {case_dir}")
        return None

    # 3) Identificar a pasta correta dentro de VTK/
    if not os.path.exists(vtk_path):
        print(f"❌ Pasta VTK não encontrada em {case_dir}")
        return None

    time_dirs = [
        d
        for d in os.listdir(vtk_path)
        if os.path.isdir(os.path.join(vtk_path, d))
        and "internal.vtu" in os.listdir(os.path.join(vtk_path, d))
    ]

    if not time_dirs:
        print(f"❌ Nenhuma pasta contendo 'internal.vtu' encontrada em {vtk_path}")
        return None

    # Ordenar para pegar a última (maior tempo de simulação)
    latest_vtk_dir = sorted(
        time_dirs, key=lambda x: int("".join(filter(str.isdigit, x)))
    )[-1]
    latest_vtk_path = os.path.join(vtk_path, latest_vtk_dir)

    print(f"📂 Última pasta de tempo detectada: {latest_vtk_path}")
    return latest_vtk_path
