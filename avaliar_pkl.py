import pickle
import numpy as np
import os

def load_and_check_pkl(file_path):
    """
    Carrega o arquivo .pkl e imprime suas dimensões (shape) e o número total de elementos.
    
    Args:
        file_path (str): Caminho para o arquivo .pkl.
    """
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Erro: O arquivo '{file_path}' não existe!")
            return
        
        # Carregar os dados do arquivo .pkl
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        
        print(f"Arquivo '{file_path}' carregado com sucesso!")
        
        # Verificar se os dados carregados são um array NumPy (sem ser dicionário)
        if isinstance(data, np.ndarray):
            print(f"Dimensões do arquivo: {data.shape}")
            print(f"Número total de elementos: {np.prod(data.shape)}")
            
            # Exibir as dimensões e o número total de elementos para cada variável em dataX ou dataY
            print(f"Exemplo de dados carregados (primeiros 5 elementos): {data.flatten()[:5]}")
        else:
            print(f"Os dados carregados não são um array NumPy. Tipo encontrado: {type(data)}")
            print(f"Exemplo de dados carregados: {data[:5] if len(data) > 5 else data}")
    
    except Exception as e:
        print(f"Erro ao carregar o arquivo {file_path}: {e}")

def main():
    # Caminhos dos arquivos .pkl gerados
    dataX_file = 'postprocesses/processed_data/dataX.pkl'  # Caminho para o arquivo dataX.pkl
    dataY_file = 'postprocesses/processed_data/dataY.pkl'  # Caminho para o arquivo dataY.pkl

    # Carregar e analisar os arquivos .pkl
    print("Analisando arquivo dataX.pkl")
    load_and_check_pkl(dataX_file)

    print("\nAnalisando arquivo dataY.pkl")
    load_and_check_pkl(dataY_file)

if __name__ == "__main__":
    main()
