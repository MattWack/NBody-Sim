# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:50:54 2023

@author: mattw
"""
import moderngl_window as mdgw
import numpy as np
import glm

class SphereMesh():
    
    def __init__(self, ctx, program, material, in_pos=[0.0, 0.0, 0.0], radius=1.0, fragments=16):
        self.ctx = ctx
        self.program = program
        self.material = material
        self.voa = self._create_voa(radius, fragments)
        
        self.update_mesh_state(pos=in_pos)
        
        self.apply_properties()
        
        
    def update_mesh_state(self, pos=[0, 0, 0], rot =[0, 0, 0], scaling=[1, 1, 1]):
        
        translate = glm.mat4(np.array([[1, 0, 0, pos[0]],
                                       [0, 1, 0, pos[1]],
                                       [0, 0, 1, pos[2]],
                                       [0, 0, 0, 1]]))
        rot = glm.mat4() #Implment if you want to see planets
        scaling = glm.scale(scaling)
                           
        self.world_mat = translate
        
    def render(self):
        self.program['world_mat'].write(self.world_mat)
        self.material.texture.use()
        self.voa.render(self.program)        
        
    def destroy(self):
        self.voa.release()

    def apply_properties(self):
        
        self.program['mat_color'].value = glm.vec3(self.material.mat_color)
        
        self.program['u_texture_0'].value = 0
        if self.material.ambient:
            self.program['ambient'].value = glm.vec3(self.material.ambient)
        if self.material.mat_specular:
            self.program['mat_specular'].value = glm.vec3(self.material.mat_specular)
        if self.material.mat_shininess:
            self.program['mat_shininess'].value = self.material.mat_shininess
        

    def _create_voa(self, r, f):
        
        ## This code generates the following name for the attributes in shaders ##
        # POSITION = "in_position"
        # NORMAL = "in_normal"
        # TEXCOORD_0 = "in_texcoord_0"
        
        return mdgw.geometry.sphere(radius=r, rings=f, sectors=f)
    
        
    
        
    
    