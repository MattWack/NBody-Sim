# -*- coding: utf-8 -*-
"""
Classes representing physical objects
This set of classes represents physical objects.  It is primarily a way to 
keep track of the attributes (temperature, position, velocity, etc) of objects
in the simulator.  They are inteded for use with the  Physics classes.
"""
import Vector as vc
import numpy as np
class ThermalPhobject(object):
    '''An object that has temperature
    Attributes
    ----------
    temperature : float
        The current temperature of the object    
    '''
    
    def __init__(self,temperature):
        self.temperature = temperature
        

class GravPhobject():
    '''An object that has temperature

    Attributes
    ----------
    mass : float
        The current mass of the object    
    
    pos : Vector
        The current position of the object    
    
    vel : float
        The current velocity of the object    
    '''
    def __init__(self, mass, pos, vel):
        self.mass = mass
        if isinstance(pos, list):
            self.pos = vc.Vector.asArray(pos)
        else:
            self.pos = pos
        if isinstance(vel, list):
            self.vel = vc.Vector.asArray(vel)
        else:
            self.vel = vel
    
    @property
    def state(self):
        """
        The array for the position and velocity of the phobject.

        Returns
        -------
        6d Array
            Array in the form of [px, py, pz, vx, vy, vz].

        """
        return np.array([self.pos.x, self.pos.y, self.pos.z, 
                         self.vel.x, self.vel.y, self.vel.z])
    
    @state.setter
    def state(self, newState):
        self.pos.x = newState[0]
        self.pos.y = newState[1]
        self.pos.z = newState[2]
        self.vel.x = newState[3]
        self.vel.y = newState[4]
        self.vel.z = newState[5]
        
        
        