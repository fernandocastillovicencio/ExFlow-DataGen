import os

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Diretório onde está config.py
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))  # Diretório raiz do projeto

# Diretórios principais
TEMPLATE_DIR = os.path.join(PROJECT_DIR, "template-lam")  # Template da simulação
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")  # Diretório de saída
POSTPROCESS_DIR = os.path.join(OUTPUT_DIR, "postProcessing")  # Diretório de pós-processamento

# Diretórios específicos
SYSTEM_PATH = os.path.join(TEMPLATE_DIR, "system")  # Diretório do sistema
CLOUD_PATH = os.path.join(POSTPROCESS_DIR, "cloud")  # Caminho correto para postProcessing/cloud

# Lista de velocidades para simulação
VELOCITIES = [0.1, 0.3, 0.5, 0.8, 1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8, 3.0]

# Nome do arquivo de velocidade dentro da pasta de cada caso
U_FILE_NAME = "0/U"

# Nome do log da simulação
LOG_FILE_NAME = "log.simpleFoam"

# Definição da malha para amostragem
NPOINTS = 100
X_MIN, X_MAX, DX = -1, 3, (3 - (-1)) / NPOINTS
Y_MIN, Y_MAX, DY = -1.5, 1.5, (1.5 - (-1.5)) / NPOINTS


# Nome do arquivo de saída HDF5 (salvo dentro de cada case_dir)
HDF5_FILE_NAME = "data.h5"
