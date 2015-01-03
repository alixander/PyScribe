import os
from setuptools import setup
setup(
    name = "pyscribe",
    version = "0.1.2",
    author = "Alexander Wang",
    author_email = "alexanderw@berkeley.edu",
    description = ("PyScribe makes print debugging easier and more efficient"),
    license = "MIT",
    keywords = "python pyscribe debug print",
    url = "https://github.com/alixander/pyscribe",
    download_url = "https://github.com/alixander/pyscribe/tarbell/0.1.2",
    entry_points={
        'console_scripts': [
            'pyscribe = pyscribe.pyscribe:main',
            ],
        },
    packages=['pyscribe'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
