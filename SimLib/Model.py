# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:40:12 2023

@author: mattw
"""
import Solver as slv
import Physics as phys 
import Phobject as pho
import Phobjects as phos
import numpy as np

class Model():
    '''Base class for a physics model
    ----------
    physics : Physics
        The physics object to decribe motion of the model  
    phobject : array of Phobjects
        An object that holds positon, velocity, and mass. This is the object 
        that the physics is applied to.
    time: float
        The time where the current model is at.
    dt_max: float
        The maximum change in time the model is allowed to solve with.
    '''
    
    def __init__(self, physics, phobjects, time = 0, dt_max = .01):
        self.dt_max = dt_max
        self.physics = physics
        self.phobjects = phobjects
        self.time = time
       
    def advance(self, dt):
        """
        Advances the model by dt

        Parameters
        ----------
        dt : float
            The change in time to progress the model.

        Returns
        -------
        None.

        """
        if dt > self.dt_max:
            dt = self.dt_max
        # for obj in self.phobject:
        self.time, self.phobjects = self.physics.advance(self.time, 
                                                         self.phobjects, 
                                                               dt)
        
               
    def advance_to(self, t):
        """
        Advances the model to a time t.

        Parameters
        ----------
        t : float
            The time to advance the model to

        Returns
        -------
        None.

        """
        
        self.t, self.phobject = self.physics.advance_to(self.time, 
                                                        self.phobject, 
                                                        t)
                         
        
class Trajectory_Model(Model):
    '''A physics model to represent a projectile in a central gravitational system.
    ----------
    p0 : 3x1 array of float
        The initial position of the projectile in [x, y, z].
    v0 : 3x1 array of flaot
        The initial velocity of the projectile in [vx, vy, vz].
    grav_mass: float
        The mass of the gravitational object
    pro_mass : float
        The projectile's mass
    pro_dia : float
        The diameter of the projectile
    dt_max: float
        The maximum change in time the model is allowed to solve with.
    cur_time: float
        The time where the current model is at.
        
    '''
    
    def __init__(self, p0, v0, grav_mass, pro_mass, pro_dia, dt_max = .1, cur_time = 0):
        
        self.projectile = pho.GravPhobject(pro_mass, p0, v0)
        self.dt_max = dt_max
        self.cur_time = cur_time
        
        rk2 = slv.RK2()
        self._grav = phys.UniformGravity(rk2, grav_mass, self.dt_max, .25*pro_dia**2)
        
    
    def advance(self):
        """
        Advances the model by dt

        Returns
        -------
        None.

        """
              
        self.cur_time, self.projectile = self._grav.advance(self.cur_time, 
                                                            self.projectile, 
                                                            self.dt_max)
        
    def advance_to(self, target):
        """
        Advances the model to a given time.

        Parameters
        ----------
        target : float
            The time to advance to.

        Returns
        -------
        None.

        """
        self.projectile = self._grav.advance_to(self.cur_time, 
                                                self.projectile, 
                                                target)
        self.cur_time = target
        
class OrbitModel(Model):
    '''A physics model to represent objects in a central gravitational system.
    ----------
    e : array of float
        The eccentricity for the orbits for the objects.
    a : array of flaot
        The semi-major axis for the objects in AU.
    m: array of flaot
        The mass of the objects in Solar mass.
    dt_max: float
        The maximum change in time the model is allowed to solve with.
        
    '''
    
    def __init__(self, e, a, m, dt_max = .01):
        self.e = e
        self.a = a
        self.m = m
        self.dt_max = dt_max
        
        rk4 = slv.RK4()
        physics = phys.CentralGravity(rk4, 1, self.dt_max)
        
        
        phobject = []
        for i in range(e.size):
            pos = [self._rp(e[i], a[i]), 0, 0]
            vel = [0, self._vp(e[i], a[i]), 0]
            phobject.append(pho.GravPhobject(m[i], pos, vel))
        super().__init__(physics, phobject, 0, dt_max)
        
    def advance(self, dt):
        if dt > self.dt_max:
            dt = self.dt_max
        for obj in self.phobject:
            t, obj = self.physics.advance(self.time, obj, dt)
        self.time = t
            
    def advance_to(self, t):
        """
        Advances the model to a time t.

        Parameters
        ----------
        t : float
            The time to advance the model to

        Returns
        -------
        None.

        """
        
        for obj in self.phobject:
            self.t, obj = self.physics.advance_to(self.time, 
                                                        obj, 
                                                        t)
                                                       
        
        
    def _vp(self, e, a):
        """
        Helper function to calculate perihelion velocity

        Parameters
        ----------
        e : float
            The eccentricity of the orbit.
        a : float
            Semi-Major axis of orbit.

        Returns
        -------
        float
            The perihelion velocity.

        """
        return (4*np.pi**2/a * ((1+e)/(1-e)))**(1/2)
    
    def _rp(self, e, a):
        """
        Helper function to calculate perihelion radius

        Parameters
        ----------
        e : float
            The eccentricity of the orbit.
        a : float
            Semi-Major axis of orbit.

        Returns
        -------
        float
            The perihelion radius.

        """
        return a*(1-e)
     
        
        
        
class SolarSystem(OrbitModel):
    '''A physics model to represents mercury, venus, mars, earth, and a comet 
    in a central gravitational system.
    ----------
    dt_max: float
        The maximum change in time the model is allowed to solve with.
        
    '''
    
    def __init__(self, dt_max = .01):
               
        mercury_e = 0.205630
        mercury_a = 0.387098
        mercury_m = 1.65912519e-7
        
        
        venus_e = 0.006772
        venus_a = 0.723332 
        venus_m = 2.4472e-6
        
        earth_e = 0.0167086
        earth_a = 1.0000010178
        earth_m = 3.00273e-6
        
        mars_e = 0.093
        mars_a = 1.5237
        mars_m = 3.2256e-7
        
        
        comet_e = .9
        comet_a = 3
        comet_m = 2.5e-16
        
        e_arr = np.array([mercury_e, venus_e, earth_e, mars_e, comet_e])
        a_arr = np.array([mercury_a, venus_a, earth_a, mars_a, comet_a])
        m_arr = np.array([mercury_m, venus_m, earth_m, mars_m, comet_m])
        
        super().__init__(e_arr, a_arr, m_arr, dt_max)
        
        obj = self.phobject
        
        self.mercury = obj[0]
        self.venus = obj[1]
        self.earth = obj[2]
        self.mars = obj[3]
        self.comet = obj[4]
        
        
        
    def _vp(self, e, a):
        """
        Helper function to calculate perihelion velocity
    
        Parameters
        ----------
        e : float
            The eccentricity of the orbit.
        a : float
            Semi-Major axis of orbit.
    
        Returns
        -------
        float
            The perihelion velocity.
    
        """
        return (4*np.pi**2/a * ((1+e)/(1-e)))**(1/2)

    def _rp(self, e, a):
        """
        Helper function to calculate perihelion radius
    
        Parameters
        ----------
        e : float
            The eccentricity of the orbit.
        a : float
            Semi-Major axis of orbit.
    
        Returns
        -------
        float
            The perihelion radius.
    
        """
        return a*(1-e)


class NBodyModel(Model):
    '''A physics model that simulates N-Body gravitational interactions 
    ----------
    phob_list : List of Phobjects
        A list of phobjects to simulate
    dt_max: float
        The maximum change in time the model is allowed to solve with.
        
    '''
    
    def __init__(self, phob_list, dt_max = .01):
        self.dt_max = dt_max
        rk4 = slv.RK4()
        physics = phys.NBody(rk4, self.dt_max)
        
        super().__init__(physics, phos.Phobjects(phob_list).phobject_mat, 0, dt_max)
        
    def add_phobject(self, phob):
        if isinstance(phob, list):
            self.phobjects = np.vstack((self.phobjects, np.array(phob)))
            
        
        
        
        
class NBodySolarModel(NBodyModel):
    '''A physics model to represents the Sun, mercury, venus, mars, earth, and 
    a comet in a N-Body gravitational system.
    ----------
    dt_max: float
        The maximum change in time the model is allowed to solve with.
        
    '''
    def __init__(self, dt_max = .01):
        
        
        mercury_e = 0.205630
        mercury_a = 0.387098
        mercury_m = 1.65912519e-7
        
        
        venus_e = 0.006772
        venus_a = 0.723332 
        venus_m = 2.4472e-6
        
        earth_e = 0.0167086
        earth_a = 1.0000010178
        earth_m = 3.00273e-6
        
        mars_e = 0.093
        mars_a = 1.5237
        mars_m = 3.2256e-7
        
        
        
        comet_e = .9
        comet_a = 3
        comet_m = 2.5e-16
        
        e_arr = np.array([mercury_e, venus_e, earth_e, mars_e, comet_e])
        a_arr = np.array([mercury_a, venus_a, earth_a, mars_a, comet_a])
        m_arr = np.array([mercury_m, venus_m, earth_m, mars_m, comet_m])
        
        ## Adding the Sun 
        phobject_list = [pho.GravPhobject(1, [0,0,0], [0,0,0])]
        
        for i in range(e_arr.size):
            pos = [self._rp(e_arr[i], a_arr[i]), 0, 0]
            vel = [0, self._vp(e_arr[i], a_arr[i]), 0]
            phobject_list.append(pho.GravPhobject(m_arr[i], pos, vel))
        
        super().__init__(phobject_list, dt_max)
        
        
        get_phobjects = self.phobjects.get_phob
        
        self.sun = get_phobjects(0)
        self.mercury = get_phobjects(1)
        self.venus = get_phobjects(2)
        self.earth = get_phobjects(3)
        self.mars = get_phobjects(4)
        self.comet = get_phobjects(5)
        
        
        
    def _vp(self, e, a):
        """
        Helper function to calculate perihelion velocity
    
        Parameters
        ----------
        e : float
            The eccentricity of the orbit.
        a : float
            Semi-Major axis of orbit.
    
        Returns
        -------
        float
            The perihelion velocity.
    
        """
        return (4*np.pi**2/a * ((1+e)/(1-e)))**(1/2)

    def _rp(self, e, a):
        """
        Helper function to calculate perihelion radius
    
        Parameters
        ----------
        e : float
            The eccentricity of the orbit.
        a : float
            Semi-Major axis of orbit.
    
        Returns
        -------
        float
            The perihelion radius.
    
        """
        return a*(1-e)
    
    
class AsteroidModel(NBodyModel):
    
    
    def __init__(self, numAsteroids=100, dt_max = .01):
        
        self.numAsteroids = numAsteroids
        
        mercury_e = 0.205630
        mercury_a = 0.387098
        mercury_m = 1.65912519e-7
        
        
        venus_e = 0.006772
        venus_a = 0.723332 
        venus_m = 2.4472e-6
        
        earth_e = 0.0167086
        earth_a = 1.0000010178
        earth_m = 3.00273e-6
        
        mars_e = 0.093
        mars_a = 1.5237
        mars_m = 3.2256e-7
        
        jupiter_e = 0.0489
        jupiter_a = 5.2038
        jupiter_m = 9.54588e-4
        
        comet_e = .9
        comet_a = 3
        comet_m = 2.5e-16
        
        e_arr = np.array([mercury_e, venus_e, earth_e, mars_e, jupiter_e, comet_e])
        a_arr = np.array([mercury_a, venus_a, earth_a, mars_a, jupiter_a, comet_a])
        m_arr = np.array([mercury_m, venus_m, earth_m, mars_m, jupiter_m, comet_m])
        
        ## Adding the Sun 
        phobject_list = [pho.GravPhobject(1, [0,0,0], [0,0,0])]
        for i in range(e_arr.size):
            pos = [self._rp(e_arr[i], a_arr[i]), 0, 0]
            vel = [0, self._vp(e_arr[i], a_arr[i]), 0]
            phobject_list.append(pho.GravPhobject(m_arr[i], pos, vel))
        
        
        asteroidList = self._createAsteroids(numAsteroids)
        
        for asteroid in asteroidList:
            phobject_list.append(pho.GravPhobject(asteroid[2], asteroid[0], asteroid[1]))
            
            
        super().__init__(phobject_list, dt_max)
            
        
            
        
        
    def reset(self):
        """
        Resets the model to the inital positons and re-randomizes the asteroids

        Returns
        -------
        None.

        """
        self.__init__(self.numAsteroids, self.dt_max)
        
        
    def _createAsteroids(self, n):
        """
        Creates random postions of the asteroids with a normal distrbution centered at 3 AU

        Parameters
        ----------
        n : int
            Number of asteroids to create.

        Returns
        -------
        asteroidList : list
            A list where each index contians the postion, velocity, and mass of each asteroid.

        """
        
        radius = np.random.normal(loc = 3.0, scale = 0.4, size = n)
        angle = np.random.rand(n)*np.pi*2
        
        mass = 6.25e-10
        average_speed = 2.698304
        
        
        x = radius*np.cos(angle)
        y = radius *np.sin(angle)
        
        mag = (x**2 + y**2)**(-1/2)
        
        
        vel_x = -mag*y*average_speed
        vel_y = mag*x*average_speed
        
        
        
        asteroidList = [0 for i in range(n)]
        for i in range(n):
            asteroidList[i] = [[x[i], y[i], 0], [vel_x[i], vel_y[i], 0], mass]
            
        return asteroidList    
            
    
    
    def _vp(self, e, a):
        """
        Helper function to calculate perihelion velocity
    
        Parameters
        ----------
        e : float
            The eccentricity of the orbit.
        a : float
            Semi-Major axis of orbit.
    
        Returns
        -------
        float
            The perihelion velocity.
    
        """
        return (4*np.pi**2/a * ((1+e)/(1-e)))**(1/2)

    def _rp(self, e, a):
        """
        Helper function to calculate perihelion radius
    
        Parameters
        ----------
        e : float
            The eccentricity of the orbit.
        a : float
            Semi-Major axis of orbit.
    
        Returns
        -------
        float
            The perihelion radius.
    
        """
        return a*(1-e)
            
        
        
        
        

    
    
    
    

    