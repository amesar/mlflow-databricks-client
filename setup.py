from setuptools import setup, find_packages

setup(
    name="mlflow_databricks_client",
    version="1.0.0",
    author="Andre Mesarovic",
    description="Python client for Databricks-specific MLflow API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url="https://github.com/amesar/mlflow-reports",
    project_urls={
        "Bug Tracker": "https://github.com/amesar/mlflow-databricks-client/issues",
        "Documentation": "https://github.com/amesar/mlflow-databricks-client",
        "Source Code": "https://github.com/amesar/mlflow-databricks-client"
    },
    python_requires = ">=3.8",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    install_requires=[
        "mlflow[skinny]",
        "databricks-sdk",
        "wheel"
    ],
    extras_require= { "tests": [ "pytest","pytest-html>=3.2.0" ] },
    license = "Apache License 2.0",
    keywords = "mlflow ml ai",
    classifiers = [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ]
)
