# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:50:30 2023

@author: mattw
"""
import moderngl as mgl
import moderngl_window as mglw
import pygame as pg
import mesh
import scene
import shaderProgram
import numpy as np
import material

class Render3D():

    def __init__(self, model, win_size, render_speed = 1/1000):
        self.model = model
        self.win_size = win_size
        self.render_speed = render_speed
        
        pg.init()
   
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.screen = pg.display.set_mode((self.win_size),  flags = pg.OPENGL | pg.DOUBLEBUF)  
   

        self.ctx = mgl.create_context()  
        self.ctx.enable(flags=mgl.DEPTH_TEST)
        
        mglw.activate_context(ctx = self.ctx)
        
        self.scene = scene.Scene(self.ctx, win_size)
        
        
    def createBasicScene(self):
        
        ## memory management ##
        
        ####
        basic = material.Material(self.ctx, 'earth.jpg', [0, 0,0], xflip = True)
        program = shaderProgram.ShaderProgram(self.ctx).program
        sphere1 = mesh.SphereMesh(self.ctx, program, basic, radius= .5, fragments=16)
        mesh_arr = [sphere1, sphere1, sphere1, sphere1,sphere1, sphere1 ]
        
        
        
        self.scene.add_mesh_arr(mesh_arr)
        self.scene.update_camera_specs([0, 0, 2])
        
        
        
    def createSolorScene(self, numAsteroids):
        
        pg.event.set_grab(True)      
        planet_shine = 5.0
        planet_specular = .5
        planet_ambient = .3
        
        self.scene.update_backround_color([0, 0, 0 ])
        self.scene.camera.set_mouse_sens(.4)
        
        sun_text = material.Material(self.ctx, 'sun.jpg', [1, 1, 1], ambient=1)
        
        mercury_text = material.Material(self.ctx, 'mercury.jpg', [1, 1, 1],
                                         ambient=planet_ambient,
                                         mat_shininess=planet_shine, 
                                         mat_specular= planet_specular)
        
        venus_text = material.Material(self.ctx, 'venus.jpg', [1, 1, 1],
                                       ambient=planet_ambient,
                                       mat_shininess=planet_shine, 
                                       mat_specular= planet_specular)
        
        earth_text = material.Material(self.ctx, 'earth.jpg', [1, 1, 1],
                                       ambient=planet_ambient,
                                       mat_shininess=planet_shine, 
                                       mat_specular= planet_specular)
        
        mars_text = material.Material(self.ctx, 'mars.jpg', [1, 1, 1],
                                      ambient=planet_ambient,
                                      mat_shininess=planet_shine, 
                                      mat_specular= planet_specular)
        
        jupiter_text = material.Material(self.ctx, 'jupiter.jpg', [1, 1, 1],
                                      ambient=planet_ambient,
                                      mat_shininess=planet_shine, 
                                      mat_specular= planet_specular)
        asteroid_text = material.Material(self.ctx, 'asteroid.jpg', [1, 1, 1],
                                      ambient=planet_ambient,
                                      mat_shininess=planet_shine, 
                                      mat_specular= planet_specular)
        
        comet_text = material.Material(self.ctx, 'comet.jpg', [1, 1, 1],
                                       ambient=planet_ambient,
                                       mat_shininess=planet_shine, 
                                       mat_specular= planet_specular)
        
        
        planet_shader = shaderProgram.ShaderProgram(self.ctx, 'planet').program
        sun_shader = shaderProgram.ShaderProgram(self.ctx, 'sun').program
        
        sun = mesh.SphereMesh(self.ctx, sun_shader, sun_text, 
                              radius = .1, fragments = 40)
        mercury = mesh.SphereMesh(self.ctx, planet_shader, mercury_text, 
                                  radius = .01, fragments=32)
        venus = mesh.SphereMesh(self.ctx, planet_shader, venus_text, 
                                radius = .03, fragments = 32)
        earth = mesh.SphereMesh(self.ctx, planet_shader, earth_text, 
                                radius = .03, fragments = 32)
        mars = mesh.SphereMesh(self.ctx, planet_shader, mars_text, 
                                radius = .025, fragments = 32)
        jupiter = mesh.SphereMesh(self.ctx, planet_shader, jupiter_text, 
                                radius = .06, fragments = 35)
        comet = mesh.SphereMesh(self.ctx, planet_shader, comet_text, 
                                radius = .005, fragments = 32)
        asteroid = mesh.SphereMesh(self.ctx, planet_shader, asteroid_text, 
                                radius = .005, fragments = 32)
        
        
        
        
        
        mesh_arr = [sun, mercury, venus, earth, mars, jupiter, comet]
        for i in range(numAsteroids):   
            mesh_arr.append(asteroid)
            
        self.scene.add_mesh_arr(mesh_arr)
        self.scene.add_light([0,0,0], [1, 1, 1])
        self.scene.update_camera_specs([1, 0, 0])
        self.scene.camera.set_velocity(0.0005 / self.render_speed)
        
        
        
        
        
    
        
        
        

    def render(self, dt):  
            self.ctx.clear(self.scene.backround_color[0], 
                           self.scene.backround_color[1],
                           self.scene.backround_color[2])
            self.scene.render(dt, self.model.phobject[:, :3])
            self.model.advance(dt)
            
            # print(self.scene.camera.forward)
            
            
            pg.display.flip()
