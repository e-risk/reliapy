#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='reliapy',
    version="1.0.0",
    url='https://github.com/e-risk/reliapy',
    description="Reliapy is a python toolbox focused in the risk and reliability analysis of engineering systems",
    author="Ketson R. M. dos Santos",
    author_email="ketson.santos@gmail.com",
    license='MIT',
    platforms=["OSX", "Windows", "Linux"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["*.pdf"]},
    install_requires=[
        "numpy", "scipy", "matplotlib", "scikit-learn", 'fire'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)
