#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='reliapy',
    version="0.1.0",
    url='https://github.com/e-risk/reliapy',
    description="UQpy is a general purpose toolbox for Uncertainty Quantification",
    author="Ketson R. M. dos Santos",
    author_email="reliapy.py@@gmail.com",
    license='MIT',
    platforms=["OSX", "Windows", "Linux"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["*.pdf"]},
    install_requires=[
        "numpy", "scipy", "matplotlib"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)
