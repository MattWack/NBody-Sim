# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:50:46 2023

@author: mattw
"""
import light
import camera
import glm

class Scene:
    
    def __init__(self, ctx, win_size):
        self.ctx = ctx 
        self.win_size = win_size
        self.meshes = []
        self.camera = camera.Camera(ctx, win_size, [0, 0, 0])
        self.backround_color = (.3, .1, .4) #RGB
        
    def add_mesh_arr(self, mesh_arr):
        for mesh in mesh_arr:
            mesh.program['proj_mat'].write(self.camera.get_proj_mat())
            self.meshes.append(mesh)
        
            
    def add_light(self, light_pos, light_color):
        self.light = light.Light(light_pos, light_color) 
        
    def update_camera_specs(self, in_pos, fov=60.0, near=.1, far=100.0, yaw=-90, pitch=0):
        
        self.camera = camera.Camera(self.ctx, self.win_size, in_pos, fov=fov, 
                                    near=near, far=far, yaw=yaw, pitch=pitch)
        if len(self.meshes) != 0:
            for mesh in self.meshes:
                mesh.program['proj_mat'].write(self.camera.get_proj_mat())
                
    def update_backround_color(self, new_bc):
         
        self.backround_color = new_bc
        
    
    def render(self, dt, mesh_positions):
        
        self.camera.update(dt)
        
        
            
        
        for i, mesh in enumerate(self.meshes):
            
            mesh.update_mesh_state(mesh_positions[i, :])
            mesh.program['view_mat'].write(self.camera.get_view_mat())
            
            # The Sun shader does not use these, so this is my dirty solution
            if i > 0: 
                mesh.program['camera_position'].write(self.camera.position)
                
                mesh.program['light_position'].value = glm.vec3(self.light.pos)
                mesh.program['light_color'].value = glm.vec3(self.light.color)
            mesh.render()
        
        
    
    
     
    
            
            
        