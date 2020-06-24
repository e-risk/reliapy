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
``Random`` is the module for ``reliapy`` used to define and simulate random variables and random processes.

This module contains the classes and methods necessary to define and simulate random variables and processes. 

The module currently contains the following classes:
* ``StateLimit``: Class used to compute the state limit euqation g(X).
* ``DiffusionMaps``: Class for multi point data-based dimensionality reduction.
"""

import numpy as np
import scipy as sp
from scipy import stats

class Variables:
    
    def __init__(self, distributions=None):
        
        if isinstance(distributions,list):
            self.distributions = distributions
            self.nrv = len(distributions)
        elif distributions is None:
            self.distributions = ['norm']
            self.nrv = 1
        else:
            raise TypeError('RELIAPY: not valid type for distributions.')
            
        if self.nrv != len(self.distributions):
            raise ValueError('RELIAPY: nrv must be equal to the number of distributions.')
        
    def probability(self, x=None, q=None, parameters=None, opt='pdf'):
        
        if opt is 'icdf':
            opt = 'ppf'
            
        numq = 0
        if isinstance(q,list):
            numq = len(q)
        elif isinstance(q,(int,float)):
            numq = 1
            q = [q]
            
        prob_out = []
        for i in range(self.nrv):
        
            params = parameters[i]
            
            if isinstance(eval('stats.'+self.distributions[i]),stats.rv_discrete):
                if opt is'pdf':
                    opt='pmf'
                       
                if opt is 'logpdf':
                    opt='logpmf'
                    
            else: 
                if opt is'pmf':
                    opt='pdf'
                       
                if opt is 'logpmf':
                    opt='logpdf'

            fun_scipy = eval('stats.'+self.distributions[i]+'.'+opt)
            
            if opt in ('pdf','pmf','cdf','logpdf','logpmf','logcdf','sf'):
                if x is None:
                    raise ValueError('RELIAPY: x cannot be NoneType.')
                prob_out.append(fun_scipy(x, **params))
                
            if opt in ('ppf','isf'):
                
                if q is None:
                    raise ValueError('RELIAPY: q cannot be NoneType.')
                    
                for j in range(numq):
                    if q[j]<0 or q[j]>1:
                        raise ValueError('RELIAPY: q cannot be lower than zero or larger than one.')
                    
                prob_out.append(fun_scipy(q, **params))
                
            elif opt is 'stats':
                mean_x, var_x, skew_x, kurt_x = fun_scipy(moments='mvsk', **params)
                prob_out.append([mean_x, var_x, skew_x, kurt_x])
        
        return prob_out
    
    
    def sampling(self, nsamples=1, parameters=None):
        
        if not isinstance(nsamples,int):
            raise TypeError('RELIAPY: nsamples must integer.')
            
        if nsamples<1:
            raise ValueError('RELIAPY: nsamples must be larger than or equal to one.')
    
        samples_out = []
        for i in range(self.nrv):
            params = parameters[i]
            fun_scipy = eval('stats.'+self.distributions[i]+'.rvs')
            samples = fun_scipy(size=nsamples, random_state=None, **params)
            samples_out.append(samples)
        
        return samples_out
    
class Processes:
    
    def __init__(self):
        raise NotImplementedError('RELIAPY: please, wait for the next version!')