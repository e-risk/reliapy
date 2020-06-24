# UQpy is distributed under the MIT license.
#
# Copyright (C) 2020  -- Ketson R. M. dos Santos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
``Model`` is the module for ``reliapy`` used to run the state limit equation. It is also an interface with external 
programs.

This module contains the classes and methods necessary to compute the value of the state limit equation. Further, 
it also serve as the interface between ``reliapy`` and external programs (e.g., FE codes).

The module currently contains the following classes:
* ``StateLimit``: Class used to compute the state limit euqation g(X).
"""

import numpy as np


class StateLimit:
    """
    Use this class to call the state limit equation.

    The class ``StateLimit`` is used to manage the execution of the state limit equation considering that
    it can be passed by the user as a callable object and can be used as an interface to an external code,
    such as FE programs. 

    **Input:**
    * **state_limit** (`callable`)
        Callable object containing the state limit functions.
        
    * **system** (`bool`)
        Boolean variable  if True the output will also show the value of each state limit equation composing
        the system.

    **Attributes:**
    * **g** (`list`)
        Value(s) of the state limit equation(s) (equations if a system is considered).

    **Methods:**
    """

    def __init__(self, state_limit=None, state_limit_grad=None):

        if callable(state_limit):
            self.state_limit = state_limit
        else:
            raise TypeError('RELIAPY: state_limit must be callable.')

        self.g = []

    def run(self, samples=None):
        
        """
        Compute the value of the state limit equation(s).
        
        The method ``run`` will receive the samples as input variables. The samples are stored in a list and this list
        can be composed by samples of a random variables or a random process. The user is totally responsible for the 
        shape of the input variables. Moreover, the state limit equations are send to the module as a callable object
        programmed by the user externally.

        **Input:**
        * **samples** (`list`)
            Samples passed by the user to the state limit equation.
        
        **Output/Returns:**
        
        * **g** (`list`)
            Value(s) of the state limit equation(s) (equations if a system is considered).
        """

        # Check if samples are provided
        if samples is None:
            raise ValueError('RELIAPY: Samples must be provided as input.')
        elif isinstance(samples, list):
            nsim = len(samples)  # This assumes that the number of rows is the number of simulations.
        else:
            raise ValueError('RELIAPY: Samples must be passed as a list')

        # Run python model
        g = []
        for i in range(nsim):

            state_lim = self.state_limit(samples[i])

            g.append(state_lim)

        return g
    
    
    def drun(self, samples=None):
        
        """
        Compute the gradient of the state limit equation(s).
        
        The method ``drun`` will receive the samples as input variables to compute the gradient of the state limit
        equation. The samples are stored in a list and this list can be composed by samples of a random variables 
        or a random process. The user is totally responsible for the shape of the input variables. Moreover, the 
        state limit equations are send to the module as a callable object programmed by the user externally.

        **Input:**
        * **samples** (`list`)
            Samples passed by the user to the state limit equation.
        
        **Output/Returns:**
        
        * **g** (`list`)
            Value(s) of the state limit equation(s) (equations if a system is considered).
        """

        # Check if samples are provided
        if samples is None:
            raise ValueError('RELIAPY: Samples must be provided as input.')
        elif isinstance(samples, list):
            nsim = len(samples)  # This assumes that the number of rows is the number of simulations.
        else:
            raise ValueError('RELIAPY: Samples must be passed as a list')

        # Run python model
        dg = []
        for i in range(nsim):

            state_lim_grad = self.state_limit_grad(samples[i])

            dg.append(state_lim_grad)

        return dg
