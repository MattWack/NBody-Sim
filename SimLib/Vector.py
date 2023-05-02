# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:09:54 2023

@author: Matthew Wackerfuss
"""
import numpy as np
class Vector():
    """Class the represents a vector.
    
    Attributes
    ----------
    x : float
        x-coord

    y : float
        y-coord
        
    z : float
         z-coord
    
    """
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    
    @property
    def rho(self):
        """
        Radius Coord of the vector

        Returns
        -------
        flaot
            The values of rho.

        """
        return np.sqrt(self.x**2+self.y**2+self.z**2)
    
    @rho.setter
    def rho(self, new_rho):
        theta = self.theta
        phi = self.phi
        self.x = new_rho*np.sin(phi)*np.cos(theta)
        self.y = new_rho*np.sin(phi)*np.sin(theta)
        self.z = new_rho*np.cos(phi)
            
       
    @property
    def theta(self):
        """
        Angle between x-y plane coord. of the vector.

        Returns
        -------
        float
            The theta value.

        """
        if (self.x != 0):
            return np.arctan2(self.y,self.x)
        else:
            return 0
    
    @theta.setter
    def theta(self, new_theta):
        rho = self.rho
        phi = self.phi
        self.x = rho*np.sin(phi)*np.cos(new_theta)
        self.y = rho*np.sin(phi)*np.sin(new_theta)
        self.z = rho*np.cos(phi)
        
    
    @property
    def phi(self):
        """
        The angle between z-y plane coord. of the vector.

        Returns
        -------
        float
            The phi value.

        """
        if (self.z != 0):
            return np.arccos(self.z/self.rho)
        else:
            return 0
      
     
    @phi.setter
    def phi(self, new_phi):
        theta = self.theta
        rho = self.rho
        self.x = rho*np.sin(new_phi)*np.cos(theta)
        self.y = rho*np.sin(new_phi)*np.sin(theta)
        self.z = rho*np.cos(new_phi)
        
        
    @classmethod
    def asArray(cls, arr):
        """
        Class method that takes an array of x, y, z values and creates a vector object  

        Parameters
        ----------
        arr : array
            A 3D array in the form of [x y z].

        Returns
        -------
        Vector
            The new Vector from [x y z].

        """
        return Vector(arr[0], arr[1], arr[2])
     
    @classmethod
    def asPolar(cls, arr):
        """
        Creates Vector object from Array of polar values

        Parameters
        ----------
        arr: 3D Array
            An array in the form of [rho, theta, phi]
        Returns
        -------
        Vector
            New Vector object with given coords

        """
        rho = arr[0]
        theta = arr[1]
        phi = arr[2]
        
        xnew = rho*np.cos(theta)*np.sin(phi)
        ynew = rho*np.sin(phi)*np.sin(theta)
        znew = rho*np.cos(phi)
        return Vector(xnew, ynew, znew)
    
    def __add__(self, other):
        """
        Adds two vectors with normal vector addition.

        Parameters
        ----------
        other : Vector
            The other vector to add.

        Returns
        -------
        Vector:
            The resulting vector from vector addition.
            

        """
        new_x = other.x + self.x
        new_y = other.y + self.y
        new_z = other.z + self.z
        return Vector(new_x, new_y, new_z)
    
              

    def __mul__(self, scalar):    
        """
        Multiplies a vector and a scalar 

        Parameters
        ----------
        scalar : float
            scalar to multiply.

        Returns
        -------
        Vector 
            A new Vector with the form of v(s*x, s*y, s*z).

        """
        new_x = self.x*scalar
        new_y = self.y*scalar
        new_z = self.z*scalar
        return Vector(new_x,new_y, new_z)
    
    
def main():
     v1 = Vector.asArray([1, 1, 1])
     v2 = Vector.asArray([-3, 1, 1])
     
     v3 = v1+v2
     print(v3.x)
     print(v3.rho)
     v4 = v3*5    
     print(v4.rho)
     print(v4.theta)
     v4.theta = 2
     print(v4.theta)
     
     v5 = Vector.asArray([0,3,2])
     print(v5.z)
     
     v6 = Vector.asPolar([1, 1, 1])
     print(v6.theta)
     print(v6.phi)
     v6.phi = 3
     print(v6.phi)
     v6.y = 1
     print(v6.phi)

if __name__ == "__main__":
    main()