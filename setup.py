from setuptools import setup, find_packages

setup(
    name="supply-chain-mcs",
    version="0.1.0",
    description="Inventory Risk & Optimization Engine with ML and Monte Carlo Simulation",
    author="",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.19.0",
        "scikit-learn>=0.24.0",
        "xgboost>=1.3.0",
        "lightgbm>=3.1.0",
        "matplotlib>=3.0.0",
        "prophet>=1.0",
        "requests>=2.0.0",
        "pyarrow>=1.0.0",
        "duckdb>=0.4.0",
    ],
    include_package_data=True,
    package_data={
        "": ["data/*", "data/raw/*", "data/processed/*"],
    },
)
