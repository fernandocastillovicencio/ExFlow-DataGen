import os
import numpy as np
import pickle
import random
import subprocess
import shutil
import matplotlib.pyplot as plt

# 📂 Diretórios principais
CASES_DIR = "cases"
TEMPLATE_SAMPLE_DICT = "templates/postprocessing/system/sampleDict"
PROCESSED_DIR = "processed_data"

# 🔄 Escolher um caso aleatório
cases = [c for c in os.listdir(CASES_DIR) if os.path.isdir(os.path.join(CASES_DIR, c))]
selected_case = random.choice(cases)
case_path = os.path.join(CASES_DIR, selected_case)
processed_path = os.path.join(case_path, "processed")

print(f"🔄 Testando pós-processamento no caso aleatório: {selected_case}")
print(f"📂 Caminho real da pasta do caso: {case_path}")

# 📌 1️⃣ Copiar `sampleDict` para o `system/` do case
system_path = os.path.join(case_path, "system")
sampledict_path = os.path.join(system_path, "sampleDict")

if not os.path.exists(sampledict_path):
    print(f"📂 Copiando `sampleDict` para {system_path}...")
    shutil.copy(TEMPLATE_SAMPLE_DICT, sampledict_path)
    print("✅ `sampleDict` copiado com sucesso!")

# 📌 2️⃣ Adicionar `sampleDict` ao `controlDict` automaticamente
control_dict_path = os.path.join(system_path, "controlDict")

# Lê o arquivo `controlDict`
with open(control_dict_path, "r") as f:
    control_dict_lines = f.readlines()

# Verifica se já existe uma seção `functions`
if not any("functions" in line for line in control_dict_lines):
    print("🔄 Adicionando `functions` no `controlDict`...")
    control_dict_lines.append('\nfunctions\n{\n    #include "sampleDict"\n}\n')

# Salva a versão modificada do `controlDict`
with open(control_dict_path, "w") as f:
    f.writelines(control_dict_lines)

print("✅ `controlDict` atualizado para incluir `sampleDict`!")

# 📌 3️⃣ Executar `foamToVTK` dentro da pasta do case
print("🔄 Executando `foamToVTK -latestTime`...")
subprocess.run(["foamToVTK", "-latestTime"], cwd=case_path, check=True)

# 📌 4️⃣ Executar `postProcess -func sample` para extrair os dados
print("🔄 Executando `postProcess -func sample -latestTime`...")
subprocess.run(
    ["postProcess", "-func", "sample", "-latestTime"], cwd=case_path, check=True
)

# 📌 5️⃣ Caminho dos arquivos extraídos pelo OpenFOAM
postprocess_dir = os.path.join(case_path, "postProcessing/sample/latestTime")
files = {"Ux": "sampleGrid_U.xy", "Uy": "sampleGrid_U.xy", "p": "sampleGrid_p.xy"}

# 📌 Criar diretório para salvar os dados processados
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 📌 6️⃣ Converter os arquivos `.xy` para `.npy`
for key, filename in files.items():
    filepath = os.path.join(postprocess_dir, filename)
    output_npy = os.path.join(PROCESSED_DIR, f"{key}.npy")

    if os.path.exists(filepath):
        print(f"🔄 Convertendo {filename} para {key}.npy ...")
        data = np.loadtxt(filepath)  # Carregar os valores do OpenFOAM
        np.save(output_npy, data[:, -1])  # Salvar apenas os valores
        print(f"✅ Salvo: {output_npy}")
    else:
        print(f"❌ Arquivo não encontrado: {filepath}")

# 📌 7️⃣ Salvar os arquivos `.pkl`
Ux = np.load(os.path.join(PROCESSED_DIR, "Ux.npy"))
Uy = np.load(os.path.join(PROCESSED_DIR, "Uy.npy"))
p = np.load(os.path.join(PROCESSED_DIR, "p.npy"))

dataY = np.stack([Ux, Uy, p], axis=0)

with open(os.path.join(PROCESSED_DIR, "dataY.pkl"), "wb") as f:
    pickle.dump(dataY, f)

print("✅ Arquivo `dataY.pkl` salvo com sucesso!")

# 📌 8️⃣ Remover apenas imagens antigas na pasta `processed_data/`
for file in os.listdir(PROCESSED_DIR):
    file_path = os.path.join(PROCESSED_DIR, file)
    if os.path.isfile(file_path) and file.endswith(".png"):
        os.remove(file_path)


# 📌 9️⃣ Gerar imagens dos dados extraídos
def plot_field(data, title, filename):
    plt.figure(figsize=(8, 6))
    plt.imshow(data.reshape(172, 79), cmap="jet", origin="lower")
    plt.colorbar(label="Magnitude")
    plt.title(title)
    plt.xlabel("X (grid points)")
    plt.ylabel("Y (grid points)")
    plt.grid(False)
    plt.savefig(os.path.join(PROCESSED_DIR, filename))
    plt.close()


plot_field(Ux, "Velocidade Ux", "Ux_sampled.png")
plot_field(Uy, "Velocidade Uy", "Uy_sampled.png")
plot_field(p, "Pressão", "p_sampled.png")

print("✅ Todas as imagens foram geradas e salvas em `processed_data/`!")
