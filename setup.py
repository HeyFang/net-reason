from setuptools import setup, find_packages

setup(
    name="net-reason",
    version="0.1.0",
    description="Network & Linux error diagnosis CLI — AIKR project",
    packages=find_packages(),
    package_data={
        "": ["../data/*.json"],
    },
    include_package_data=True,
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "netreason=netreason.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)
