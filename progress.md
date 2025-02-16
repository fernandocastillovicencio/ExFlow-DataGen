ExFlow-DataGen/
└── src/
    ├── modules/
    │   ├── geometry/               # 🟠 Geometry Module
    │   │   ├── obstacles.py        # 🔹 Obstacle generation (ellipse, triangle, quadrilateral, combinations)
    │   │   ├── domain.py           # 🔹 Domain creation in Salome
    │   │   ├── __init__.py
    │   ├── meshing/                # 🟢 Mesh Generation Module
    │   │   ├── generate_mesh.py
    │   │   ├── __init__.py
    │   ├── execution/              # 🔵 OpenFOAM Execution Module
    │   │   ├── run_simulation.py
    │   │   ├── __init__.py
    │   ├── postprocessing/         # 🟣 Post-Processing Module
    │   │   ├── process_results.py
    │   │   ├── __init__.py
    ├── run_pipeline.py             # 🔥 Full pipeline execution
    ├── test_modules.py             # 🛠 Individual module testing
