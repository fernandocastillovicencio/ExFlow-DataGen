from scipy.spatial import cKDTree
import numpy as np
import pickle


def compute_SDF(points, grid_x, grid_y):
    """
    Calcula a Signed Distance Function (SDF1) do obstáculo.

    Args:
        points (array): Pontos do domínio.
        grid_x (array): Coordenadas X da malha estruturada.
        grid_y (array): Coordenadas Y da malha estruturada.

    Returns:
        array: Matriz SDF de tamanho (172, 79).
    """
    X, Y = np.meshgrid(grid_x, grid_y, indexing="ij")  # Criar grade com indexing='ij'

    tree = cKDTree(points)
    sdf = tree.query(np.c_[X.ravel(), Y.ravel()])[0]  # Obter distância
    sdf = sdf.reshape(len(grid_x), len(grid_y))  # Garantir formato correto

    return sdf  # Removida transposição desnecessária


def compute_flow_region(sdf):
    """
    Gera a matriz de flow region channel.

    Args:
        sdf (array): Matriz SDF.

    Returns:
        array: Flow region channel.
    """
    if sdf.shape != (172, 79):
        raise ValueError(f"Erro: sdf tem formato {sdf.shape}, esperado (172, 79)")

    flow_region = np.ones((172, 79))
    flow_region[sdf < 1e-3] = 0  # Obstáculo
    flow_region[0, :] = 3  # Entrada
    flow_region[-1, :] = 4  # Saída
    flow_region[:, 0] = 2  # Freestream lateral
    flow_region[:, -1] = 2  # Freestream lateral

    return flow_region


def save_dataX(sdf1, flow_region, sdf2, output_file="dataX.pkl"):
    """
    Empacota os dados de entrada no formato adequado e salva em .pkl.

    Args:
        sdf1 (array): SDF do obstáculo.
        flow_region (array): Canal de fluxo.
        sdf2 (array): SDF das paredes laterais.
        output_file (str): Nome do arquivo de saída.
    """
    dataX = np.stack([sdf1, flow_region, sdf2], axis=0)  # (3, 172, 79)
    dataX = np.expand_dims(dataX, axis=0)  # (1, 3, 172, 79)

    with open(output_file, "wb") as f:
        pickle.dump(dataX, f)

    print(f"✅ {output_file} salvo!")
