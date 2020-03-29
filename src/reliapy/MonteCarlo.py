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
import scipy as sp
import numpy as np

########################################################################################################################
########################################################################################################################
#                                            Monte Carlo Simulation                                                    #
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

    def __init__(self, object=None):

        self.object = distance_object
        
    # Calculate the distance on the manifold
    def MCS(self, nsim=10):

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

        

        return nsim

    # ==================================================================================================================
   
