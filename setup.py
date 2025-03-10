import os

from setuptools import setup, PEP420PackageFinder

base_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_dir, 'README.md')) as fid:
    description = fid.read()

PROJECT_NAME = "TANGLE"
REQUIRED_PY = ">= 3.9.0"

version = {}
with open(os.path.join(base_dir, 'tngl', '__version__.py')) as fid:
    exec(fid.read(), version)

setup(
    name=PROJECT_NAME,
    version=version['__version__'],
    description="A Signal analysis and recording took to pick up spectrum signal analysis anomalies and the like.",
    python_requires=REQUIRED_PY,
    long_description=description,
    url='git@github.com:/ForwardML/tangle.git',
    author='FORWARD ML LLC',
    platforms=['Ubuntu 20.04', 'Arch Linux (Kernel 5.10)'],
    packages=PEP420PackageFinder.find(include=["tngl"]),
    zip_safe=False,
    install_requires=[
        "matplotlib",
        "numpy",
        "scipy",
        "pandas",
        "requests",
        "tqdm"
    ],
    extras_require={},
    include_package_data=True,
    entry_points={
        'console_scripts':[
            "record_sweep=tngl.console.record:main"
        ]
    }
)
