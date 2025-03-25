import os

# Diretório base do case OpenFOAM
BASE_PATH = "template-lam"

# Caminhos do sistema
SYSTEM_PATH = os.path.join(BASE_PATH, "system")  # Onde será salvo o arquivo sample
POSTPROCESS_PATH = os.path.join(BASE_PATH, "postProcessing")  # Onde OpenFOAM salvará os arquivos .xy
OUTPUT_NPY_PATH = os.path.join(BASE_PATH, "postProcessing/Ux_field.npy")  # Arquivo final de saída
CLOUD_PATH = os.path.join(POSTPROCESS_PATH, "cloud")  # Definir corretamente o caminho
PLOT_PATH = os.path.join(POSTPROCESS_PATH, "plots")  


# Definição da malha para amostragem
NPOINTS = 100
X_MIN, X_MAX, NX = -1, 3, NPOINTS  # Faixa e número de pontos no eixo X
Y_MIN, Y_MAX, NY = -1.5, 1.5, NPOINTS  # Faixa e número de pontos no eixo Y

DX = (X_MAX - X_MIN) / NX
DY = (Y_MAX - Y_MIN) / NY



# 🔹 Caminho do arquivo `sample`
SAMPLE_FILE_PATH = os.path.join(SYSTEM_PATH, "sample")

# 🔹 Nome do arquivo de entrada gerado pelo OpenFOAM
CLOUD_FILE_NAME = "ref_point_p_U.xy"  # Nome do arquivo exato esperado

# 🔹 Nome do arquivo de saída HDF5 (será salvo dentro da pasta correta)
HDF5_FILE_NAME = "data.h5"
