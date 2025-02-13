# ExFlow-DataGen

## Overview
**ExFlow-DataGen** is a modular Python-based framework designed to generate simulation data from Computational Fluid Dynamics (CFD) using OpenFOAM, specifically for external flow simulations. This software automates the generation of STL geometries, meshing, CFD simulations, and post-processing to create structured datasets for deep learning models.

## Features
- **Automated STL Geometry Generation**: Uses Salome to generate solid geometries with varied shapes.
- **Mesh Generation**: Implements `cfMesh` to create computational meshes from STL files.
- **CFD Simulation Execution**: Runs OpenFOAM’s `simpleFoam` solver for external flow calculations.
- **Data Export & Processing**: Converts simulation outputs to VTK format and extracts structured data.
- **Machine Learning Data Preparation**: Generates `dataX.pkl` (input features) and `dataY.pkl` (ground truth outputs) optimized for deep learning.
- **Modular Object-Oriented Design**: Encapsulated functionalities ensure code maintainability and extensibility.
- **Logging & Error Handling**: Comprehensive logging system to track execution at each stage.

## Project Structure
```
ExFlow-DataGen/
│── config/                   # Configuration files
│   ├── openfoam_template/    # OpenFOAM base files (simpleFoam, cfMesh)
│   ├── mesh_config.json      # Configuration for meshing (cfMesh settings)
│   ├── solver_config.json    # Solver configuration for OpenFOAM (simpleFoam)
│
│── src/                      # Source code for the project
│   │── geometry/              # Geometry-related classes
│   │   ├── geometry_generator.py  # Class for STL generation (Salome)
│   │   ├── stl_merger.py          # Class for merging STL files
│   │
│   │── simulation/            # Simulation-related classes
│   │   ├── case_manager.py        # Handles OpenFOAM case copying
│   │   ├── mesher.py              # Runs cfMesh to generate the mesh
│   │   ├── solver.py              # Runs simpleFoam solver
│   │   ├── result_exporter.py     # Exports results (VTK format)
│   │
│   │── postprocessing/        # Data processing classes for Machine Learning
│   │   ├── sdf_computer.py        # Computes Signed Distance Function (SDF)
│   │   ├── dataset_preparer.py    # Formats dataX.pkl and dataY.pkl
│   │
│   │── utils/                 # Utility functions and helpers
│   │   ├── logging_utils.py       # Handles logging
│   │   ├── file_utils.py          # File management utilities
│   │
│   ├── main.py                # Main script orchestrating all processes
│
│── logs/                     # Execution logs
│── output/                   # Stores the final output files
│   ├── cases/                # Individual simulation case results
│   ├── dataset/              # Final dataX.pkl and dataY.pkl
│
│── requirements.txt           # List of dependencies
│── README.md                  # Documentation
```

## Installation
### Requirements
- Python 3.8+
- OpenFOAM (with `simpleFoam` solver)
- cfMesh (for mesh generation)
- Salome (for STL geometry creation)
- NumPy, SciPy, OpenCV (for data processing)
- ParaView (optional, for VTK visualization)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/fernandocastillovicencio/ExFlow-DataGen.git
   cd ExFlow-DataGen
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure OpenFOAM and Salome are installed and accessible in the system's environment variables.

## Usage
### Running the Full Pipeline
Execute the main script to run the full pipeline from STL generation to dataset creation:
```bash
python src/main.py
```
### Running Individual Modules
- Generate STL geometries:
  ```bash
  python src/geometry/geometry_generator.py
  ```
- Run meshing:
  ```bash
  python src/simulation/mesher.py
  ```
- Execute CFD simulation:
  ```bash
  python src/simulation/solver.py
  ```
- Export results:
  ```bash
  python src/simulation/result_exporter.py
  ```
- Process dataset:
  ```bash
  python src/postprocessing/dataset_preparer.py
  ```

## Output Format
The final dataset consists of two structured files:
- **`dataX.pkl` (Model Input):** Contains geometry and physics-based input data.
  - Signed Distance Function (SDF)
  - Flow Region Channel (domain mask)
  - Shape: `(N, 3, 172, 79)`
    - `N`: Number of samples (e.g., 981 simulations)
    - `3`: Channels (SDF 1, SDF 2, Domain Mask)
    - `172 x 79`: Spatial resolution

- **`dataY.pkl` (Model Output):** Ground-truth CFD results.
  - Ux (Velocity X), Uy (Velocity Y), Pressure (p)
  - Shape: `(N, 3, 172, 79)`

## Logging
Execution logs are stored in `logs/`, detailing each step:
```bash
logs/
├── geometry_generation.log
├── meshing.log
├── simulation.log
├── postprocessing.log
```
These logs help debug failures and track performance.

## Contributions
Contributions are welcome! Please follow the standard GitHub workflow:
1. Fork the repository
2. Create a new branch
3. Make changes and commit
4. Submit a pull request

## License
MIT License. See `LICENSE` file for details.

## Contact
For issues or suggestions, please open an issue on GitHub or contact the maintainer at `castillovicencio@aol.com`.
