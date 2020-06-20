#!/usr/bin/env python

from distutils.core import setup
setup(
  name = 'reliapy',         # How you named your package folder (MyLib)
  packages = ['src'],   # Chose the same as "name"
  version = '0.1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Reliapy is a python toolbox focused in the risk and reliability analysis of engineering systems',   # Give a short description about your library
  author = 'Ketson R. M. dos Santos',                   # Type in your name
  author_email = 'reliapy.py@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/e-risk/reliapy/archive/v_010.tar.gz',    # I explain this later on
  keywords = ['Structural Reliability', 'Stochastic Process', 'Probability'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Scientific/Engineering :: Mathematics',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Natural Language :: English',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
