import os

# Diretório base do case OpenFOAM
BASE_PATH = "template-lam"

# Caminhos do sistema
SYSTEM_PATH = os.path.join(BASE_PATH, "system")  # Onde será salvo o arquivo sample
POSTPROCESS_PATH = os.path.join(BASE_PATH, "postProcessing")  # Onde OpenFOAM salvará os arquivos .xy
OUTPUT_NPY_PATH = os.path.join(BASE_PATH, "postProcessing/Ux_field.npy")  # Arquivo final de saída
SAMPLE_PATH = os.path.join(POSTPROCESS_PATH, "sample/5")  # Onde o script de amostragem irá rodar
# Definição da malha para amostragem
NPOINTS = 100
X_MIN, X_MAX, NX = -3, 5, NPOINTS  # Faixa e número de pontos no eixo X
Y_MIN, Y_MAX, NY = -1, 1, NPOINTS  # Faixa e número de pontos no eixo Y

DX = (X_MAX - X_MIN) / NX
DY = (Y_MAX - Y_MIN) / NY

# Caminho do arquivo `sample` que será criado dentro de system/
SAMPLE_FILE_PATH = os.path.join(SYSTEM_PATH, "sample")
