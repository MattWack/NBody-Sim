# -*- coding: utf-8 -*-
"""
The Physics base class and its children
This set of classes implements various differential equations that represent 
different physical environments.  They are inteded for use with the 
differential equation solving classes derived from Solver.
"""
import Vector as vc
import numpy as np
import scipy.constants as c
class Physics(object):
    """Base class for Physics objects. 
    
    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation
        
    """
    def __init__(self,solver):
        self.sovler = solver

    def advance(self,body,t,dt):
        """Advance the body one time step
        
        This advance implementation in the Physics base class is a stub.
        It exists only to define the interface for the advance method.
        Classes derived from Physics should define their own versions of 
        advance following the same interface.
        
        Parameters
        ----------
        t : float
            The current time
            
        body : Body
            An instance of a class derived from Body
            
        dt : float
            The amount of time to advance. (the time step)
        
        Returns
        -------
        time : float
            The new time

        body : Body
            The body advanced one time step        
        """
        print("Physics.advance is a stub!  This line should never be executed")
        return          # Do nothing, simply return.
    
    def diff_eq(self,t,T):
        """The cooling differential equation
        
        This diff_eq implementation in the Physics base class is a stub.
        It exists only to define the interface for the advance method.
        Classes derived from Physics should define their own versions of 
        advance following the same interface.

        Parameters
        ----------
        T : float
            The current temperature of the object
            
        t : float
            The current time
        
        Returns
        -------
        dTdt : float
            The slope at T        
        """
        
        
        
        
        print("Physics.diff_eq is a stub!  This line should never be executed")
        return          # Do nothing, simply return.

    
class Cooling(Physics):
    """Implements cool cooling.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation
        
    Ta : float
        The ambient temperature
        
    k : float
        The cooling coefficient
    
    """
    
    def __init__(self,solver,Ta,k):
        self.solver = solver
        self.Ta = Ta
        self.k = k
        
    def advance(self,t,phobject,dt):
        """
        Advances to the next temperature and time 

        Parameters
        ----------
        t : flaot
            time for the differentail equation.
        phobject : Phoobject
            The physics object that the temperature is being calculated on.
        dt : flaot
            The time between T and Tnext.

        Returns
        -------
        tnext : float
            The next time.
        phobject : Phobject
            The phobject with an updated temperature at tnext.

        """
        
        T = phobject.temperature
        tnext, phobject.temperature = self.solver.advance(t, T, dt, self.diff_eq)
        return tnext, phobject
       
            
    def diff_eq(self,t,T):
        """
        The cooling diff_eq

        Parameters
        ----------
        t : float
            The time to evaluate cooling curve.
        T : flaot
            The temperature of system.

        Returns
        ------
        float
            The change of temperature.

        """
               
        return self.k*(self.Ta - T)


class NBody(Physics):
    
    def __init__(self, solver, dt_max = .01):
        
        self.solver = solver
        self.dt_max = dt_max
        
        
        
    def diff_eq(self, t, F):
        
        pos_mat = F[:, :3, None]
        ms = F[:, 6]
        rows = np.shape(pos_mat)[0]
        
        back_dup_pos = np.ones((rows, 3, rows)) * pos_mat
        down_dup_pos = back_dup_pos.T
        
        pos_diff_mat = (back_dup_pos - down_dup_pos)
    
        radii = np.sum(pos_diff_mat**2, axis = 1)
        np.fill_diagonal(radii, 1)
        
        radii = (radii**(-3/2))[:, None, :] * np.ones((rows, 3, rows))
        
        partial_sums = pos_diff_mat*radii * ms[:, None, None]
        
        acc = np.sum(partial_sums, axis = 0).T * 4 * np.pi**2
        
        ret = np.concatenate((F[:, 3:6], acc, np.zeros(rows)[:, None]), axis = 1)
        
        return ret
        
        
        
        
    
    
    
    def advance(self, t, phobject, dt):
        """
        Advances to the next velocity, postition, and time of the object in gravity

        Parameters
        ----------
        t : flaot
            time for the differentail equation.
        phobject : Phoobject
            The physics object that the velocity and position is being calculated on.
        dt : flaot
            The time after the given velocity and position.

        Returns
        -------
        tnext : float
            The next time.
        phobject : Phobject
            The phobject with an updated velocity and position at tnext.
        """
        
        tnext, phobject = self.solver.advance(t, 
                                              phobject, 
                                              dt, 
                                              self.diff_eq)
        return tnext, phobject
    
    
    def advance_to(self, oldt, phobject, newt):
        """
        Function that solves the diff_eq at a given time from an old time at a known value.

        Parameters
        ----------
        oldt : float
            The last time that the diff_eq was solved at.
        phobject : Phobject
            The phobject that is being solved for it's new value.
        newt : float
            The new time that the diff_eq is solved at.

        Returns
        -------
        Phobject
            The Phobject with the updated values.

        """
        
        sign = np.sign(newt-oldt)
        
        while(np.abs(oldt-newt) > self.dt):
            oldt, phobject[:, :-1] = self.solver.advance(oldt, 
                                                       phobject[:, :-1], 
                                                       sign*self.dt_max, 
                                                       self.diff_eq)
            
        oldt, phobject[:, :-1] = self.solver.advance(oldt, 
                                                   phobject[:, :-1], 
                                                   newt-oldt, 
                                                   self.diff_eq)
        
        return newt, phobject
        
    
    
    

class CentralGravity(Physics):
    """Class for a central gravity system

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation
        
    mass : float
        The mass of object that causes the centralized gravity

    
    """
    def __init__(self, solver, mass, dt):
        self.solver = solver
        self.mass = mass
        self.dt = dt
        
    def diff_eq(self, t, F):
        """
        The diff_eq describing acceloration in unform gravational field.

        Parameters
        ----------
        t : float
            Time.
        F : 6d Array
            An array descring an object in the graviational fields. Array needs to be [px, py, pz, vx, vy, vz].

        Returns
        -------
        Array
            The array returning velocty and acceloration of object in the form of [vx,vy,vz,ax,ay,az].

        """
        radius = vc.Vector.asArray(F[0:3]).rho
        G = 4*np.pi**2
        constant = -1*G*self.mass/radius**3
        ret = np.array([F[3], F[4], F[5], constant*F[0], constant*F[1], constant*F[2]])
        return ret
    
    def advance(self, t, phobject, dt):
        """
        Advances to the next velocity, postition, and time of the object in gravity

        Parameters
        ----------
        t : flaot
            time for the differentail equation.
        phobject : Phoobject
            The physics object that the velocity and position is being calculated on.
        dt : flaot
            The time after the given velocity and position.

        Returns
        -------
        tnext : float
            The next time.
        phobject : Phobject
            The phobject with an updated velocity and position at tnext.
        """
        
        tnext, phobject.state = self.solver.advance(t, 
                                                    phobject.state, 
                                                    dt, 
                                                    self.diff_eq)
        return tnext, phobject
    
    
    def advance_to(self, oldt, phobject, newt):
        """
        Function that solves the diff_eq at a given time from an old time at a known value.

        Parameters
        ----------
        oldt : float
            The last time that the diff_eq was solved at.
        phobject : Phobject
            The phobject that is being solved for it's new value.
        newt : float
            The new time that the diff_eq is solved at.

        Returns
        -------
        Phobject
            The Phobject with the updated values.

        """
        
        sign = np.sign(newt-oldt)
        
        while(np.abs(oldt-newt) > self.dt):
            oldt, phobject.state = self.solver.advance(oldt, 
                                                       phobject.state, 
                                                       sign*self.dt, 
                                                       self.diff_eq)
            
        oldt, phobject.state = self.solver.advance(oldt, 
                                                   phobject.state, 
                                                   newt-oldt, 
                                                   self.diff_eq)
        
        return newt, phobject
    
        






class UniformGravity(Physics):
    """Class for gravity where R>>h
    
    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation
     mass : float
         The mass of object that causes the uniform gravity
     drag : float
        The coeffient for drag

    """
    
    def __init__(self, solver, mass, max_dt = .1, drag = 0):
        self.solver = solver
        self.mass = mass
        self.max_dt = max_dt
        self.drag = drag
        

    def diff_eq(self, t, F):
        """
        The differential equation describing an object in uniform gravity

        Parameters
        ----------
        t : time
            Time when to return value of differntial equation.
        F : 6d Array
            An array descring an object in the graviational fields. Array needs to be [px, py, pz, vx, vy, vz].

        Returns
        -------
        Array
            The array returning velocty and acceloration of object in the form of [vx,vy,vz,ax,ay,az].

        """
        radius = 6378.1e3  # Radius of the Earth
        gravConstant = 1*c.G*self.mass/radius**2
        velocityMag = vc.Vector(F[3], F[4], F[5]).rho
        ai = -1*self.drag*velocityMag*F[3]/self.phobject_mass
        aj = -1*self.drag*velocityMag*F[4]/self.phobject_mass - gravConstant
        ak = -1*self.drag*velocityMag*F[5]/self.phobject_mass - gravConstant
        
        return np.array([F[3], F[4], F[5], ai, aj, ak])
        
    
    
    def advance(self, t, phobject, dt):
        """
        Advances to the next velocity, postition, and time of the object in gravity

        Parameters
        ----------
        t : flaot
            time for the differentail equation.
        phobject : Phoobject
            The physics object that the velocity and position is being calculated on.
        dt : flaot
            The time after the given velocity and position.

        Returns
        -------
        tnext : float
            The next time.
        phobject : Phobject
            The phobject with an updated velocity and position at tnext.
        """
        self.phobject_mass = phobject.mass
        tnext, phobject.state = self.solver.advance(t, phobject.state, dt, self.diff_eq)
        return tnext, phobject
    
    
    def advance_to(self, oldt, phobject, newt):
        """
        Function that solves the diff_eq at a given time from an old time at a known value.

        Parameters
        ----------
        oldt : float
            The last time that the diff_eq was solved at.
        phobject : Phobject
            The phobject that is being solved for it's new value.
        newt : float
            The new time that the diff_eq is solved at.

        Returns
        -------
        Phobject
            The Phobject with the updated values.

        """
        sign = np.sign(newt-oldt)
        
        while(np.abs(oldt-newt) > self.max_dt):
            oldt, phobject = self.advance(oldt, 
                                               phobject, 
                                               sign*self.max_dt) 
                                                    
            
        oldt, phobject = self.advance(oldt, 
                                           phobject, 
                                           newt-oldt)
        
        return phobject     
     
     
     
     
     
     
     
     
     
     
     