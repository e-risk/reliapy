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
This module contains the classes and methods to perform the point wise and multi point data-based dimensionality
reduction via projection onto the Grassmann manifold and Diffusion Maps, respectively. Further, interpolation in the
tangent space centered at a given point on the Grassmann manifold can be performed.
* Grassmann: This class contains methods to perform the projection of matrices onto the Grassmann manifold where their
             dimensionality are reduced and where standard interpolation can be performed on a tangent space.
* DiffusionMaps: In this class the diffusion maps create a connection between the spectral properties of the diffusion
                 process and the intrinsic geometry of the data resulting in a multiscale representation of the data.
"""

from UQpy.Surrogates import Krig
from Utilities import *
import scipy as sp
import numpy as np
import itertools
from scipy.interpolate import LinearNDInterpolator
from os import path
import math

import scipy.sparse as sps
import scipy.sparse.linalg as spsl
import scipy.spatial.distance as sd


########################################################################################################################
########################################################################################################################
#                                            Grassmann Manifold                                                        #
########################################################################################################################
########################################################################################################################


class MonteCarlo:
    """
    Project matrices onto the Grassmann manifold and create a tangent space where standard interpolation is performed.
    This class contains methods to perform the projection of matrices onto the Grassmann manifold via singular value
    decomposition(SVD) where their dimensionality are reduced. Further, the mapping from the Grassmannian to a tangent
    space centered at a given reference point (exponential mapping) as well as the mapping from the tangent space to the
    manifold (logarithmic mapping). Moreover, a interpolation can be performed in the tangent space. Further, additional
    quantities such as the Karcher mean, the distance on the manifold, and the kernel defined on the Grassmann manifold
    can be obtained.
    **References:**
    1. Jiayao Zhang, Guangxu Zhu, Robert W. Heath Jr., and Kaibin Huang, "Grassmannian Learning: Embedding Geometry
       Awareness in Shallow and Deep Learning", arXiv:1808.02229 [cs, eess, math, stat], Aug. 2018.
    2. D.G. Giovanis, M.D. Shields, "Uncertainty quantification for complex systems with very high dimensional response
       using Grassmann manifold variations", Journal of Computational Physics, Volume 364, Pages 393-415, 2018.
    **Input:**
    :param distance_object: It specifies the name of a function or class implementing the distance on the manifold.
                            Default: None
    :type distance_object: str
    :param distance_script: The filename (with extension) of a Python script implementing dist_object
                            (only for user defined metrics).
                            Default: None
    :type distance_script: str
    :param kernel_object: It specifies the name of a function or class implementing the Grassmann kernel.
                          Default: None
    :type distance_object: str
    :param kernel_script: The filename (with extension) of a Python script implementing kernel_object
                          (only for user defined metrics).
                          Default: None
    :type distance_script: str
    :param interp_object: It specifies the name of the function or class implementing the interpolator.
                          Default: None
    :type interp_object: str
    :param interp_script: The filename (with extension) of the Python script implementing of interp_object
                          (only for user defined interpolator).
                          Default: None
    :type interp_script: str
    **Authors:**
    Authors: Ketson R. M. dos Santos, Dimitris G. Giovanis
    Last modified: 03/26/20 by Ketson R. M. dos Santos
    """

    def __init__(self, distance_object=None, distance_script=None, kernel_object=None, kernel_script=None,
                 interp_object=None,
                 interp_script=None, karcher_object=None, karcher_script=None):

        # Distance.
        self.distance_script = distance_script
        self.distance_object = distance_object
        if distance_script is not None:
            self.user_distance_check = path.exists(distance_script)
        else:
            self.user_distance_check = False

        if self.user_distance_check:
            try:
                self.module_dist = __import__(self.distance_script[:-3])
            except ImportError:
                raise ImportError('There is no module implementing a distance.')

        # Kernels.
        self.kernel_script = kernel_script
        self.kernel_object = kernel_object
        if kernel_script is not None:
            self.user_kernel_check = path.exists(kernel_script)
        else:
            self.user_kernel_check = False

        if self.user_kernel_check:
            try:
                self.module_kernel = __import__(self.kernel_script[:-3])
            except ImportError:
                raise ImportError('There is no module implementing a Grassmann kernel.')

        # Interpolation.
        self.interp_script = interp_script
        self.interp_object = interp_object
        if interp_script is not None:
            self.user_interp_check = path.exists(interp_script)
        else:
            self.user_interp_check = False

        if self.user_interp_check:
            try:
                self.module_interp = __import__(self.interp_script[:-3])
            except ImportError:
                raise ImportError('There is no module implementing the interpolation.')

        # Karcher mean.
        self.karcher_script = karcher_script
        self.karcher_object = karcher_object
        if karcher_script is not None:
            self.user_karcher_check = path.exists(karcher_script)
        else:
            self.user_karcher_check = False

        if self.user_karcher_check:
            try:
                self.module_karcher = __import__(self.karcher_script[:-3])
            except ImportError:
                raise ImportError('There is no module implementing an optimizer to find the Karcher mean.')

    # Calculate the distance on the manifold
    def distance(self, *argv, **kwargs):

        """
        Estimate the distance of points on the Grassmann manifold.
        This method computes the pairwise distance of points projected on the Grassmann manifold. The input arguments
        are passed through a list of arguments (argv) containing a list of lists or a list of numpy arrays. Further,
        the user has the option either to pass the rank of each list or numpy array or to let the method compute them.
        When the user call this method a list containing the pairwise distances is returned as an output argument where
        the distances are stored as [{0,0},{0,1},{0,2},...,{1,0},{1,1},{1,2}], where {a,b} corresponds to the distance
        between the points 'a' and 'b'. Further, users are asked to provide the distance definition when the class
        Grassmann is instatiated. The current built-in options are the Grassmann, chordal, procrustes, and projection
        distances, but the users have also the option to implement their own distance definition.
        **Input:**
        :param argv: Matrices (at least 2) corresponding to the points on the Grassmann manifold.
        :type  argv: list of arguments
        :param kwargs: Contains the keyword for the user defined rank. If a list or numpy ndarray containing the rank of
               each matrix is not provided, the code will compute them using numpy.linalg.matrix_rank.
        :type kwargs: dictionary of arguments
        **Output/Returns:**
        :param distance_list: Pairwise distance.
        :type distance_list: list
        """

        nargs = len(argv[0])
        psi = argv[0]

        if 'rank' in kwargs.keys():
            ranks = kwargs['rank']
        else:
            ranks = None

        # Initial tests
        #-----------------------------------------------------------
        if ranks is None:
            ranks = []
            for i in range(nargs):
                ranks.append(np.linalg.matrix_rank(psi[i]))
        elif type(ranks) != list and type(ranks) != np.ndarray:
            raise TypeError('rank MUST be either a list or ndarray.')
            
        if nargs < 2:
            raise ValueError('Two matrices or more MUST be provided.')
        elif len(ranks) != nargs:
            raise ValueError('The number of elements in rank and in the input data MUST be the same.')
        #------------------------------------------------------------
            
        # Define the pairs of points to compute the Grassmann distance.
        indices = range(nargs)
        pairs = list(itertools.combinations(indices, 2))

        if self.user_distance_check:
            if self.distance_script is None:
                raise TypeError('distance_script cannot be None')

            exec('from ' + self.distance_script[:-3] + ' import ' + self.distance_object)
            distance_fun = eval(self.distance_object)
        else:
            if self.distance_object is None:
                raise TypeError('distance_object cannot be None')

            distance_fun = eval("Grassmann." + self.distance_object)

        distance_list = []
        for id_pair in range(np.shape(pairs)[0]):
            ii = pairs[id_pair][0]  # Point i
            jj = pairs[id_pair][1]  # Point j

            rank0 = int(ranks[ii])
            rank1 = int(ranks[jj])

            x0 = np.asarray(psi[ii])[:, :rank0]
            x1 = np.asarray(psi[jj])[:, :rank1]

            dist = distance_fun(x0, x1)

            distance_list.append(dist)

        return distance_list

    # ==================================================================================================================
    # Built-in metrics are implemented in this section. Any new built-in metric must be implemented
    # here with the decorator @staticmethod.

    @staticmethod
    def grassmann_distance(x0, x1):

        """
        Estimate the Grassmann distance.
        One of the distances defined on a manifold is the Grassmann distance implemented herein. As the user gives the
        distance definition when the class Grassmann is instantiated the method 'distance' uses this information to call
        the respective distance definition.
        **Input:**
        :param x0: Point on the Grassmann manifold.
        :type  x0: list or numpy array
        :param x1: Point on the Grassmann manifold.
        :type  x1: list or numpy array
        **Output/Returns:**
        :param distance: Grassmann distance between x0 and x1.
        :type distance: float
        """

        l = min(np.shape(x0))
        k = min(np.shape(x1))
        rank = min(l, k)

        r = np.dot(x0.T, x1)
        (ui, si, vi) = svd(r, rank)
        index = np.where(si > 1)
        si[index] = 1.0
        theta = np.arccos(si)
        distance = np.sqrt(abs(k - l) * np.pi ** 2 / 4 + np.sum(theta ** 2))

        return distance
