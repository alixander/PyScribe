import os
from setuptools import setup
setup(
    name = "pyscribe",
    version = "0.0.1",
    author = "Alexander Wang",
    author_email = "alexanderw@berkeley.edu",
    description = ("PyScribe makes print debugging easier and more efficient"),
    license = "MIT",
    keywords = "python pyscribe debug print",
    url = "https://github.com/alixander/pyscribe",
    download_url = "https://github.com/alixander/pyscribe/tarbell/0.0.1",
    entry_points={
        'console_scripts': [
            'pyscribe = pyscribe.pyscribe:main',
            ],
        },
    packages=['pyscribe'],
    classifiers=[
        "Development Status :: 3 - Alpha"
    ],
)
