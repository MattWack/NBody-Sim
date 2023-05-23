# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:50:39 2023

@author: mattw
"""
import glm
import numpy as np
import pygame as pg

class Camera():
    '''Class for camera in a 3D scene
    ----------
    ctx : ModernGl.Context
        The context where the camera lives.
    aspect_ratio : float
        The aspect ratio of the window.
    position: glm.vec3
        The position of the camera.
    up: glm.vec3
        The up dirction of the camera. 
    right: glm.vec3
        The right direction of the camera.
    forward: glm.vec3
        Vector for where the camera is looking 
    yaw: glm.vec3
        Yaw angel of camera.
    pitch: glm.vec3
        Pitch angle of camera.
    roll: glm.vec3
        Roll angle of camera.
    fov: float
        The field of view of the camera.
    near: float
        The near clipping plane.
    far: float
        The far clipping plane.
    velocity: float
        Velocity of camera.
    mouse_sens: float
        How sensitive the camera is while moving.
    view_mat: glm.mat4
        The matrix used to transform what the camera sees into canonical space.
        This matrix depends on where in camera is looking and it's position.
    proj_mat: glm.mat4
        The matrix used to transform what the camera sees into canonical space.
        This matrix depends on the specs of the camera (near, fov, etc.)
    mounted: Boolean
        Wheather the camera is mounted upon an object.
    mounted_phobject_index: int
        An integer coordsponding to the index of the mounted phobject in the phobject matrix. 
        
    '''
    
    
    def __init__(self, ctx, win_size, in_pos, fov=60.0, near=.1, far=100.0, yaw=-90, pitch=0, roll=0):

        self.ctx = ctx
        
        self.aspect_ratio = win_size[0] / win_size[1]
        self.position = glm.vec3(in_pos)
        
        self.up = glm.vec3(0, 0, 1)
        self.right = glm.vec3(0, 1, 0)
        self.forward = glm.vec3(-1, 0, 0)
        
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        
        self.fov = fov
        self.near = near
        self.far = far
        
        self.velocity = .3
        self.mouse_sens = .1
        
        self.proj_mat = self.get_proj_mat()
        self.view_mat = self.get_view_mat()
        
        self.mounted = False
        self.mounted_phobject_index = None
        
    
        
        
        
    def get_proj_mat(self):
        """
        Method that generates the projection matrix.

        Returns
        -------
        glm.mat4
            The projection matrix.

        """
        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, 
                               self.near, self.far)
    
    def get_view_mat(self):
        """
        Method that generates the view matrix.

        Returns
        -------
        glm.mat4
            The view matrix.

        """
        
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    
    def mount_camera(self, phobject_mat):
        """
        Method that switchs the camera to mounted mode
        Parameters
        ----------
        phobject_mat : ndarray
            The matrix that holds the all the phobject attributes.

        Returns
        -------
        None.

        """
        # Setting the mounting phobject to the postion of the camera
        phobject_mat[self.mounted_phobject_index, 0:3] = [self.position.x, 
                                                          self.position.y,
                                                          self.position.z]
        # Resetting the velocity of the mounting phobject 
        phobject_mat[self.mounted_phobject_index, 3:6] = [0, 0, 0]
        
                                                      
        self.mounted = True
        
    def mount_camera_on(self, phobject_mat):
        """
        Mounts the camera to an object in the scene

        Parameters
        ----------
        phobject_mat : ndarray
            The matrix that holds the all the phobject attributes.

        Returns
        -------
        None.

        """
        
        self.position = phobject_mat[self.mounted_phobject_index, 0:3]
        
                                                      
        self.mounted = True
        
        
        
    def update(self, dt, phobject_mat):
        """
        Updates the postion of the camera

        Parameters
        ----------
        dt : float
            Chnage in time.
        phobject_mat : ndarray
            The matrix that holds the all the phobject attributes.

        Returns
        -------
        None.

        """
        
        if self.mounted:
            self.mounted_move(dt, phobject_mat[self.mounted_phobject_index, :])
        else:    
            self.standard_move(dt)

    
        self.view_mat = self.get_view_mat()

    def standard_move(self, dt):
        """
        The movement if the camrea is not gravationally interacting. 

        Parameters
        ----------
        dt : float
            Change in time.

        Returns
        -------
        None.

        """
        
        v = self.velocity * dt
        
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += v * self.forward
        if keys[pg.K_s]:
            self.position -= v * self.forward
        if keys[pg.K_a]:
            self.position -= v * self.right
        if keys[pg.K_d]:
            self.position += v * self.right
        if keys[pg.K_r]:    
            self.position += v * self.up
        if keys[pg.K_f]:
            self.position -= v * self.up
        if keys[pg.K_q]:
            self.roll += v * 100
        if keys[pg.K_e]:
            self.roll -= v * 100
            
            
        
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x*self.mouse_sens
        self.pitch -= rel_y*self.mouse_sens 
        
        
        yaw = glm.radians(self.yaw)
        pitch = glm.radians(self.pitch)
        roll = glm.radians(self.roll)
        
    
        self.forward.y = glm.cos(yaw) * glm.cos(pitch)
        self.forward.z = glm.sin(pitch)
        self.forward.x = glm.sin(yaw) * glm.cos(pitch)
        


        self.forward = glm.normalize(self.forward)
       
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3([0, 0, 1])))
        self.up = glm.normalize(glm.cross(self.right,self.forward))
        
        
            
    def mounted_move(self, dt, phob):
        """
        Movement if the camera is gravationally interacting
        Parameters
        ----------
        dt : float
            change in time.
        phob : ndarray
            The row from the phob_matrix that coordsponds to the phobject the camera is mounted upon.

        Returns
        -------
        None.

        """
        
        
        self.position = glm.vec3(phob[0:3])
        

        trust =  100 * dt
        
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            phob[3:6] += trust * self.forward
        if keys[pg.K_s]:
            phob[3:6] -= trust * self.forward
        if keys[pg.K_a]:
            phob[3:6] -= trust * self.right
        if keys[pg.K_d]:
            phob[3:6] += trust * self.right
        if keys[pg.K_r]:    
            phob[3:6] += trust * self.up
        if keys[pg.K_f]:
            phob[3:6] -= trust * self.up
        if keys[pg.K_q]:
            self.roll += trust * 100
        if keys[pg.K_e]:
            self.roll -= trust * 100
            

        
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x*self.mouse_sens
        self.pitch -= rel_y*self.mouse_sens 
        
        
        yaw = glm.radians(self.yaw)
        pitch = glm.radians(self.pitch)
        roll = glm.radians(self.roll)
        
    
        self.forward.y = glm.cos(yaw) * glm.cos(pitch)
        self.forward.z = glm.sin(pitch)
        self.forward.x = glm.sin(yaw) * glm.cos(pitch)
        


        self.forward = glm.normalize(self.forward)
       
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3([0, 0, 1])))
        self.up = glm.normalize(glm.cross(self.right,self.forward))
        
        
            
        
    