# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:08:12 2023

@author: mattw
"""
import numpy as np
import Phobject as pho
class Phobjects():
    '''A class that represents phobjects as a matrix for quicker computation.
    ----------
    phob_list: List of Phobjects
        A List of Phobjects to create a matrix.
    phobject_mat: Nd-Array
        Matrix of phobjects where columns 0-2 are position, 2-5 are velocity, 
        and 6 is mass.
        
    '''
    def __init__(self, phob_list):
        
        self.phobject_mat = np.zeros((len(phob_list), 7))
        for i, phob in enumerate(phob_list):  
            self.phobject_mat[i, 0:6] = phob.state
            self.phobject_mat[i, 6] = phob.mass
            
    def get_phob(self, index):
        """
        Function to create Phobject object from a spesified row.

        Parameters
        ----------
        index : int
            Which Phobject to create.

        Returns
        -------
        new_phob : Phobject
            The new Phobject.

        """
        phob = self.phobject_mat[index, :]
        
        new_phob = pho.GravPhobject(phob[6], 
                                    phob[:3], 
                                    phob[3:6])
        return new_phob
            
            
            
            