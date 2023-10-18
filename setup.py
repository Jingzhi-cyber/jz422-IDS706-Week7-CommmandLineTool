from setuptools import setup, find_packages

setup(
    name="mytool",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mytool=mytool.database_operations:main",
        ],
    },
    install_requires=[
        # sqlite3
    ],
)
