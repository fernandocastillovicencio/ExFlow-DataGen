# ExFlow-DataGen - Automated CFD Dataset Generation

## Project Overview
ExFlow-DataGen is a software designed to automate the generation of geometries for CFD simulations in OpenFOAM, mesh generation using cfMesh, and processing simulation results for training neural networks.

This project follows a modular architecture, enabling each step to be executed independently or as part of a fully automated pipeline. It is optimized to generate and simulate multiple geometries simultaneously, ensuring efficiency and scalability for machine learning applications.

---

## Project Directory Structure
The project is structured to ensure modularity, clear organization, and debugging efficiency.

```
ExFlow-DataGen/
├── obstacles/                 # Obstacles generated from images
│   ├── images/                # Input images representing obstacles
│   ├── stl/                   # Corresponding STL files of obstacles
├── geometries/                # Geometries generated using Salome
│   ├── geometry1/
│   │   ├── raw/               # Individual STL surfaces exported from Salome
│   │   ├── combined/          # Unified STL file of the final domain
│   │   ├── preview/           # Screenshots for validation
│   │   ├── hdf/               # Salome project files
│   ├── geometry2/
├── meshes/                    # Computational meshes generated with cfMesh
│   ├── mesh1/
│   │   ├── polyMesh/          # Mesh data
│   │   ├── log_mesh.txt       # Mesh generation log
│   ├── mesh2/
├── cases/                     # OpenFOAM simulation cases
│   ├── case1/
│   │   ├── 0/                 # Initial conditions
│   │   ├── constant/
│   │   │   ├── polyMesh/ -> ../../meshes/mesh1/polyMesh/  # Symbolic link to the mesh
│   │   │   ├── transportProperties
│   │   │   ├── turbulenceProperties
│   │   ├── system/            # Simulation configuration
│   │   ├── logs/              # Simulation logs
│   │   ├── postProcessing/    # Processed results
│   ├── case2/
├── results/                   # Processed results for ML training
│   ├── raw/                   # Raw simulation data
│   ├── processed/             # Formatted data (NumPy, CSV, etc.)
├── templates/                 # Default configuration files
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
├── src/                       # Source code
│   ├── generate_obstacles.py  # Script for generating obstacles from images
│   ├── salome/                # Salome geometry processing modules
│   ├── modules/               # Specific modules for each stage
│   │   ├── create_domain.py   # Defines the computational domain
│   │   ├── import_obstacles.py # Imports STL obstacle files into Salome
│   │   ├── boolean_subtract.py # Boolean operations for geometry processing
│   │   ├── scale_geometry.py  # Scales the geometry to match units
│   │   ├── export_surfaces.py # Exports geometry surfaces in STL format
│   ├── combine_stl.py         # STL merging and unification
│   ├── generate_mesh.py       # cfMesh automation
│   ├── run_simulation.py      # OpenFOAM execution
│   ├── process_results.py     # Post-processing for ML applications
├── logs/                      # Logs for debugging
│   ├── obstacles/             # Logs for obstacle generation
│   ├── salome/                # Logs for Salome processing
│   ├── generate_mesh/         # Logs for mesh generation
│   ├── run_simulation/        # Logs for OpenFOAM execution
│   ├── process_results/       # Logs for result post-processing
└── README.md
```

---

Modules
1. Geometry (src/modules/geometry/)
This module is responsible for creating, transforming, and saving geometric shapes in STL and PNG formats.

simples_shapes.py: Functions for generating simple shapes (circles, triangles, quadrilaterals).
transform_utils.py: Functions for rotating and stretching shapes.
shape_utils.py: Utility functions for saving shapes in STL and PNG formats.
combined_shapes.py: Functions for generating combined geometric shapes.
obstacles.py: Main script to generate and test obstacles.
2. Meshing (src/modules/meshing/)
Handles mesh generation using cfMesh for OpenFOAM simulations.

3. Solving (src/modules/solving/)
Controls the execution of the OpenFOAM solver for external flow simulations.

4. Postprocessing (src/modules/postprocessing/)
Processes simulation results for training deep learning models.

Generating Obstacles
To generate obstacles, run:
PYTHONPATH=src python src/modules/geometry/obstacles.py


## Installation and Execution

To install the dependencies and run the project, follow the steps below:

1. Clone the repository: `git clone git@github.com:fernandocastillovicencio/ExFlow-DataGen.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Run the project scripts according to the instructions in the documentation.

---

## Contact

Fernando Castillo Vicencio
[fernandocastillovicencio@gmail.com](mailto:fernandocastillovicencio@gmail.com)
[GitHub](https://github.com/fernandocastillovicencio)