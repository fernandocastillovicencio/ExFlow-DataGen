import os
from multiprocessing import Pool
from postprocess.config import OUTPUT_DIR
from postprocess.utils import is_simulation_done, get_case_dirs, run_case, run_postprocess
from postprocess.fix_missing_points import main as fix_missing_points
from postprocess.plot_sample_data import main as plot_sample_data  # Adicionando geração de gráficos
from postprocess.save_data import main as save_case_data  # Adicionando conversão para HDF5
from postprocess.combine_hfd5 import main as combine_all_data  # Adicionando etapa final


def main():
    """Executa a simulação para casos pendentes e depois roda o pós-processamento para todos os casos."""
    print("\n🔍 **Verificação do Status das Simulações** 🔍\n")

    # ---------------------------------------------------- #

    case_dirs = get_case_dirs()  # Obtém todas as pastas criadas

    if not case_dirs:
        print("⚠️ Nenhuma pasta de caso encontrada em 'output/'.")
        return

    # Identificar casos que ainda não foram processados
    pending_cases = [case for case in case_dirs if not is_simulation_done(case)]

    if pending_cases:
        print(f"🚀 Executando SimpleFoam para {len(pending_cases)} casos pendentes...\n")

        # Extrai as velocidades a partir dos nomes das pastas (ex: "U10" → 1.0)
        pending_velocities = []
        for case in pending_cases:
            try:
                velocity_str = case.replace(OUTPUT_DIR + "/U", "").replace("_", ".")
                pending_velocities.append(float(velocity_str))
            except ValueError:
                print(f"⚠️ Aviso: Não foi possível extrair a velocidade de {case}, ignorando...")

        # Executar simulações em paralelo somente se houver casos a processar
        if pending_velocities:
            with Pool(processes=len(pending_velocities)) as pool:
                pool.map(run_case, pending_velocities)

            print("\n✅ Todas as simulações pendentes foram concluídas!")
    else:
        print("✅ Todas as simulações já foram processadas!")
    # ---------------------------------------------------- #
    # # Pós-processamento sempre deve ser executado para todos os casos
    # print(f"\n🚀 Iniciando pós-processamento para {len(case_dirs)} casos...\n")

    # with Pool(processes=len(case_dirs)) as pool:
    #     pool.map(run_postprocess, case_dirs)

    # print("\n✅ Todos os casos foram pós-processados!")
    # # ---------------------------------------------------- #

    # print(f"\n🔍 Iniciando correção de pontos ausentes para {len(case_dirs)} casos...\n")

    # with Pool(processes=len(case_dirs)) as pool:
    #     pool.map(fix_missing_points, case_dirs)

    # print("\n✅ Correção de pontos ausentes concluída para todos os casos!")

    # ---------------------------------------------------- #

    # print(f"\n📊 Gerando gráficos para {len(case_dirs)} casos...\n")

    # with Pool(processes=len(case_dirs)) as pool:
    #     pool.map(plot_sample_data, case_dirs)

    # print("\n✅ Geração de gráficos concluída para todos os casos!")
    
    # ---------------------------------------------------- #

    # print(f"\n💾 Convertendo dados para HDF5 para {len(case_dirs)} casos...\n")

    # with Pool(processes=len(case_dirs)) as pool:
    #     pool.map(save_case_data, case_dirs)

    # print("\n✅ Conversão de dados para HDF5 concluída para todos os casos!")

    # # ---------------------------------------------------- #

    # print(f"\n📂 Combinando todos os dados HDF5 em um único arquivo...\n")

    # combine_all_data()  # Etapa final: Combinar todos os arquivos HDF5 em um único

    # print("\n✅ Dados de todos os casos foram combinados com sucesso!")

if __name__ == "__main__":
    main()