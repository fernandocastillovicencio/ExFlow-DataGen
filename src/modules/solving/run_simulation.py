import os
import shutil
import subprocess
from modules.solving.setup_cases import setup_cases


def clear_cases_directory(base_case_dir):
    """
    Remove completamente a pasta cases/ e recria um diretório vazio.
    """
    if os.path.exists(base_case_dir):
        shutil.rmtree(base_case_dir)
        print("🧹 Pasta 'cases/' removida com sucesso.")

    os.makedirs(base_case_dir, exist_ok=True)
    print("📂 Pasta 'cases/' recriada.")


def copy_initial_conditions(case_dir):
    """
    Copia os arquivos da pasta 0.orig para a pasta 0.

    Args:
        case_dir (str): Caminho do diretório do caso.
    """
    orig_path = os.path.join(case_dir, "0.orig")
    dest_path = os.path.join(case_dir, "0")

    if not os.path.exists(orig_path):
        print(f"⚠ Aviso: 0.orig não encontrado para {case_dir}. Pulando cópia.")
        return

    # Se a pasta 0 já existir, removê-la antes de copiar
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    shutil.copytree(orig_path, dest_path)
    print(f"📂 Condições iniciais copiadas para {case_dir}")


def run_simpleFoam(method="single"):
    """
    Executa o solver SimpleFoam.

    Args:
        method (str): Modo de execução (single ou paralelo).
    """
    if method == "single":
        subprocess.run("simpleFoam > log.simpleFoam", shell=True, check=True)
    else:
        subprocess.run(
            """
        decomposePar > log.decomposePar
        mpirun -np 12 simpleFoam -parallel > log.simpleFoam
        reconstructPar -constant > log.reconstructPar
        rm -rf processor* 
        """,
            shell=True,
            check=True,
        )


def execute_case(case_name):
    """
    Configura as condições iniciais e executa o solver SimpleFoam para um caso específico.

    Args:
        case_name (str): Nome do caso (ex: 'case_geom_001').
    """
    base_dir = os.getcwd()
    case_dir = os.path.join(base_dir, "cases", case_name)

    if not os.path.exists(case_dir):
        print(f"❌ Erro: O diretório {case_dir} não existe.")
        return

    try:
        os.chdir(case_dir)
        print(f"\n🚀 Executando simulação em: {case_dir}")

        # Copiar as condições iniciais antes de rodar o SimpleFoam
        copy_initial_conditions(case_dir)

        # Rodar SimpleFoam
        run_simpleFoam("parallel")

        # Criar arquivo case.foam
        subprocess.run("touch case.foam", shell=True, check=True)
        print(f"✅ Simulação finalizada para: {case_name}")

    except Exception as e:
        print(f"❌ Erro ao executar SimpleFoam: {e}")

    finally:
        os.chdir(base_dir)  # Retorna ao diretório original


def execute_cases():
    """
    Remove a pasta cases/, recria-a e executa todas as simulações configuradas.
    """
    base_case_dir = os.path.join(os.getcwd(), "cases")

    # Limpar a pasta cases antes de iniciar
    clear_cases_directory(base_case_dir)

    # Criar novamente as pastas dentro de cases/
    print("\n📂 Configurando casos de simulação...\n")
    setup_cases()

    # Listar casos novamente após recriação
    case_dirs = [
        d
        for d in os.listdir(base_case_dir)
        if os.path.isdir(os.path.join(base_case_dir, d))
    ]

    print(f"\n📂 Encontrados {len(case_dirs)} casos para execução.\n")

    for case in case_dirs:
        execute_case(case)


if __name__ == "__main__":
    execute_cases()
