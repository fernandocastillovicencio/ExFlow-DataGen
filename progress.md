# ExFlow-DataGen Project Progress

## Project Description
This project, **ExFlow-DataGen**, focuses on **automating the generation and simulation of external flow cases** using **Salome for geometry creation** and **OpenFOAM for CFD simulations**. The repository is hosted at:
[GitHub - ExFlow-DataGen](https://github.com/fernandocastillovicencio/ExFlow-DataGen/tree/main)

## Current Folder Structure

 cases
  cases_run
  geometries
  template
 exflow
  config
  core
  __init__.py
  __pycache__
  utils
 exflow_datagen.egg-info
  dependency_links.txt
  PKG-INFO
  requires.txt
  SOURCES.txt
  top_level.txt
 logs
  app.log
  openfoam_case_runner.log
  salome_stl_generator.log
 README.md
 requirements.txt
 scripts
  modules
  openfoam_case_runner.py
  salome_stl_generator.py
 setup.py


##  Completed Steps

### **1 STL Geometry Generation with Salome**
- Implemented **`salome_stl_generator.py`** to create **981 geometries**.
- Each geometry is saved in **cases/geometries/geom_xxxx/** with multiple STL files.
- Ensured each case **has a unique STL set**.
- Logs execution in **logs/salome_stl_generator.log**.

### **2 OpenFOAM Case Initialization**
- Implemented **`openfoam_case_runner.py`** to prepare OpenFOAM cases.
- Copies **cfMesh** configuration files from `cases/template/` to `cases/cases_run/case_xxxx/`.
- Merges **multiple STL files into a single `geom.stl`**.
- Logs execution in **logs/openfoam_case_runner.log**.

### **3 Modularization of Code**
- Refactored `openfoam_case_runner.py` into **three modules**:
  - `geometry_handler.py`  Handles STL file merging.
  - `case_initializer.py`  Manages case folder creation and template copying.
  - `meshing_runner.py`  Will handle meshing execution (next step).
- Improved maintainability and **followed software architecture best practices**.

##  Next Step: Running the Meshing Process (cfMesh)
Now that **case folders and STL files are correctly set up**, the next step is:
1. **Navigate to each case (`case_xxxx/`).**
2. **Run `cartesianMesh` (cfMesh) to generate the mesh.**
3. **Log meshing progress and handle errors.**
4. **Prepare for running `simpleFoam` simulations.**

---

##  How to Execute
### Run STL Generation:
```sh
python scripts/salome_stl_generator.py



