📅 Última Atualização: 2025-02-14
👤 Responsável: Fernando

# **📜 1. Visão Geral do Projeto**
ExFlow-DataGen é um software desenvolvido para automatizar a geração de geometrias complexas, criar malhas para CFD usando cfMesh, executar simulações no OpenFOAM e formatar os resultados para aprendizado de máquina. O software segue uma arquitetura modular, permitindo que cada etapa seja executada independentemente ou como parte de um pipeline automatizado.

## **🛠️ Tecnologias Utilizadas**
- **Salome** → Geração de geometrias 3D.
- **Python** → Automação e manipulação de arquivos.
- **cfMesh** → Geração de malha computacional.
- **OpenFOAM** → Simulação CFD.
- **Trimesh / NumPy** → Processamento de arquivos STL e resultados.

---

# **🚀 2. Estrutura Atual do Projeto**
A estrutura do projeto foi planejada para garantir **modularidade, organização clara** e **facilidade de depuração**.

```
ExFlow-DataGen/
├── obstacles/                 # Obstáculos gerados a partir de imagens
│   ├── images/                # Imagens geradas pelo script Python
│   ├── stl/                   # Arquivos STL correspondentes aos obstáculos
├── geometries/                # Geometrias geradas no Salome
│   ├── geometry1/
│   │   ├── raw/               # STL individuais exportados do Salome
│   │   ├── combined/          # STL final unificado
│   │   ├── preview/           # Capturas de tela para validação
│   │   ├── hdf/               # Arquivos do projeto Salome
│   ├── geometry2/
├── meshes/                    # Malhas geradas com cfMesh
│   ├── mesh1/
│   │   ├── polyMesh/          # Dados da malha
│   │   ├── log_mesh.txt       # Log da geração da malha
│   ├── mesh2/
│   ├── ...
├── cases/                     # Casos OpenFOAM
│   ├── case1/
│   │   ├── 0/                 # Condições iniciais
│   │   ├── constant/
│   │   │   ├── polyMesh/ -> ../../meshes/mesh1/polyMesh/  # Link simbólico para a malha
│   │   │   ├── transportProperties
│   │   │   ├── turbulenceProperties
│   │   ├── system/            # Configurações da simulação
│   │   ├── logs/              # Logs da simulação
│   │   ├── postProcessing/    # Resultados da simulação
│   ├── case2/
│   ├── ...
├── results/                   # Resultados processados para ML
│   ├── raw/                   # Dados brutos das simulações
│   ├── processed/             # Dados convertidos para ML (NumPy, CSV, etc.)
├── templates/                 # Arquivos de configuração padrão
│   ├── cfmesh/
│   │   ├── system/
│   │   │   ├── controlDict
│   │   │   ├── meshDict
│   ├── simpleFoam/
│   │   ├── 0/
│   │   │   ├── p
│   │   │   ├── U
│   │   ├── system/
│   │   │   ├── controlDict
│   │   │   ├── decomposeParDict
│   │   │   ├── fvSchemes
│   │   │   ├── fvSolution
│   │   ├── constant/
│   │   │   ├── transportProperties
│   │   │   ├── turbulenceProperties
├── src/                       # Código-fonte do projeto
│   ├── generate_obstacles.py  # Script que gera imagens e STL dos obstáculos
│   ├── salome/                # Módulos de geração de geometria no Salome
│   ├── modules/               # Módulos específicos para cada etapa
│   │   ├── create_domain.py   # Cria o domínio total
│   │   ├── import_obstacles.py # Importa obstáculos STL
│   │   ├── boolean_subtract.py # Executa operações booleanas
│   │   ├── scale_geometry.py  # Escalona a geometria
│   │   ├── export_surfaces.py # Exporta superfícies STL
│   ├── combine_stl.py         # Unificação dos STL
│   ├── generate_mesh.py       # Automação do cfMesh
│   ├── run_simulation.py      # Automação do OpenFOAM
│   ├── process_results.py     # Pós-processamento para ML
├── logs/                      # Logs organizados por etapa
│   ├── obstacles/             # Logs da geração de imagens e STL
│   ├── salome/                # Logs da importação e operações booleanas
│   ├── generate_mesh/         # Logs da geração da malha
│   ├── run_simulation/        # Logs da execução do OpenFOAM
│   ├── process_results/       # Logs do pós-processamento
└── README.md
```

---

# **📌 3. Progresso do Desenvolvimento**
Cada etapa do projeto foi documentada detalhadamente, indicando **o que foi concluído, desafios enfrentados e próximos passos**.

# **📝 5. Conclusão**
Este documento serve como um **rastreador de progresso**, garantindo que todas as etapas do desenvolvimento estejam organizadas e documentadas. A modularização do software permite **execução flexível** e **fácil depuração**.

💡 **O foco agora é finalizar os ajustes na importação de STL e melhorar a automação no OpenFOAM.**

📌 **Próxima revisão do progresso:** _(Definir uma data para reavaliar o progresso e atualizar o documento)._  

🚀 **Vamos continuar avançando!**

