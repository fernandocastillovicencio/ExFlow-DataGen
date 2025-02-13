from setuptools import setup, find_packages

setup(
    name="exflow-datagen",
    version="0.1.0",
    author="Fernando Castillo",
    description="A dataset generator for external flow simulations using OpenFOAM.",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
    ],
    python_requires=">=3.8",
)
