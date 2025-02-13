# ExFlow-DataGen

ExFlow-DataGen is an open-source project designed to automate the generation of external flow simulation cases using OpenFOAM. 
This tool enables users to generate and manage datasets for Computational Fluid Dynamics (CFD) analysis efficiently, 
focusing on external aerodynamics. The project is structured to support multiple geometries and scalable case generation.

## Features

- **Automated Case Generation**: Automates the creation of OpenFOAM cases for external flow simulations.
- **Multiple Geometries**: Supports different geometries such as airfoils, cylinders, and customizable shapes.
- **Data Export and Processing**: Exports results in structured formats for further analysis.
- **Modular Design**: Clean and maintainable architecture following software engineering best practices.
- **Logging and Error Handling**: Integrated logging system for debugging and monitoring execution.

## Project Structure

```
ExFlow-DataGen/
│── docs/                  # Documentação do projeto
│── examples/              # Casos de uso e configurações de exemplo
│── exflow/                # Código principal da aplicação (módulo principal)
│   │── __init__.py        # Indica que este é um módulo Python
│   │── core/              # Regras de negócio e lógica principal
│   │   │── __init__.py    
│   │   │── case_generator.py  # Geração de casos para OpenFOAM
│   │   │── solver.py          # Lógica de solução e automação OpenFOAM
│   │── geometry/           # Módulo para definir geometrias
│   │   │── __init__.py
│   │   │── shapes.py          # Classe base para geometrias
│   │   │── airfoil.py         # Implementação de aerofólio
│   │   │── cylinder.py        # Implementação de cilindro
│   │── io/                 # Entrada e saída de arquivos
│   │   │── __init__.py
│   │   │── foam_io.py         # Leitura e escrita de arquivos OpenFOAM
│   │   │── data_export.py     # Exportação dos dados gerados
│   │── config/             # Configurações do software
│   │   │── settings.py        # Configuração global do projeto
│   │── utils/              # Utilitários auxiliares
│   │   │── __init__.py
│   │   │── logger.py          # Sistema de logs
│── tests/                 # Testes unitários e de integração
│   │── test_geometry.py    # Testes para geometrias
│   │── test_solver.py      # Testes para solver
│   │── test_io.py          # Testes para manipulação de arquivos
│── scripts/               # Scripts auxiliares
│── setup.py               # Arquivo de instalação
│── requirements.txt       # Dependências do projeto
│── README.md              # Documentação inicial do projeto
│── .gitignore             # Arquivos a serem ignorados pelo Git
│── LICENSE                # Licença do projeto

```

## Installation

To install and set up ExFlow-DataGen, run the following commands:

```sh
git clone https://github.com/fernandocastillovicencio/ExFlow-DataGen.git
cd ExFlow-DataGen
pip install -r requirements.txt
```

## Usage

After installation, you can generate OpenFOAM cases using:

```sh
python -m exflow.core.case_generator --geometry airfoil --output ./cases/airfoil_case
```

## Contribution

Contributions are welcome! Please submit issues and pull requests following the contribution guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.