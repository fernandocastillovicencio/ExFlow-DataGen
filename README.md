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
│── docs/                  # Project documentation
│── examples/              # Example cases and configuration files
│── exflow/                # Main application module
│   │── __init__.py        # Indicates this is a Python module
│   │── core/              # Business logic and core processing
│   │   │── __init__.py    
│   │   │── case_generator.py  # OpenFOAM case generation
│   │   │── solver.py          # OpenFOAM automation and solving
│   │── geometry/           # Geometry definitions and handling
│   │   │── __init__.py
│   │   │── shapes.py          # Base class for geometries
│   │   │── airfoil.py         # Airfoil implementation
│   │   │── cylinder.py        # Cylinder implementation
│   │── io/                 # File handling and data management
│   │   │── __init__.py
│   │   │── foam_io.py         # Read/write OpenFOAM files
│   │   │── data_export.py     # Export generated data
│   │── config/             # Software configuration
│   │   │── __init__.py
│   │   │── settings.py        # Global project settings
│   │── utils/              # Auxiliary utilities
│   │   │── __init__.py
│   │   │── logger.py          # Logging system
│── tests/                 # Unit and integration tests
│   │── __init__.py
│   │── test_geometry.py    # Tests for geometries
│   │── test_solver.py      # Tests for solver
│   │── test_io.py          # Tests for file handling
│── scripts/               # Helper scripts
│   │── __init__.py
│   │── run_case.py         # Script to run a case
│── setup.py               # Installation script
│── requirements.txt       # Project dependencies
│── README.md              # Project documentation
│── .gitignore             # Git ignore rules
│── LICENSE                # Project license

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