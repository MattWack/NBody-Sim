# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:43:58 2023

@author: mattw
"""
import numpy as np
class Bisect():
    """Performs a bisection search to find a zero


    Attributes
    ----------
    right : float
        The right bracket

    left : float
        The left bracket

    right_error : float
        The error signal at the right bracket

    left_error : float
        The error signal at the left bracket

    """
    
    def __init__(self, left, right, func):
        self.left = left
        self.right = right
        self.func = func
        
        
    def iterate(self):
        """
        Function to iterate the search algorithm 

        Returns
        -------
        float 
            The new x-value.
        flaot
            The error of the iterate.

        """
        xmid = (self.right + self.left)/2
        if (self.func(xmid)*self.func(self.left)) < 0:
            self.right = xmid
        else:
            
            self.left = xmid
            
        return self.param()[0], self.error()
    
    def interate_until(self, tolerance):
        """
        Interates the bisect algorithm until a tolerance is meet.

        Parameters
        ----------
        tolerance : float
            How close the left and right values have to stop searching.

        Returns
        -------
        float 
            The new x-value.
        flaot
            The error of the iterate.

        """
        
        while self.error() > tolerance:
            self.iterate()
            
        return self.param()[0], self.error()
    
    def error(self):
        """The estimated error"""
        return np.abs(self.right - self.left)
    
    def param(self):
        """The current best estimate of the parameter"""
        xfinal = (self.right + self.left)/2
        return xfinal, self.func(xfinal)
        