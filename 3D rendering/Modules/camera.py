# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:50:39 2023

@author: mattw
"""
import glm
import pygame as pg

class Camera():
    
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
    
        
        
        
    def get_proj_mat(self):
        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, 
                               self.near, self.far)
    
    def get_view_mat(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def set_velocity(self, v):
        self.velocity = v
        
    def set_mouse_sens(self, ms):
        self.mouse_sens = ms
    
    
    def update(self, dt):
        self.move(dt)
        self.view_mat = self.get_view_mat()
        
    def move(self, dt):
        
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
        
        
            
        
        
        
            
        
    