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
import material
import skybox

class Render3D():
    '''
    Class that renders the objects in a scene
    ----------
    model : Model
        The physics model to render
    win_size : tuple
        The window size
    render_speed : float, optional
        How fast to render. The default is 1/1000
    screen : pg.Screen
        The screen to render on.
    ctx : ModerGl.Context
        The current context.
    scene : Scene
        The scene that is to be rendered.
    
    
    '''

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
        """
        Creates a basic scene of viewing.

        Returns
        -------
        None.

        """
                
        ####
        basic = material.Material(self.ctx, 'earth.jpg', [0, 0,0], xflip = True)
        program = shaderProgram.ShaderProgram(self.ctx).program
        sphere1 = mesh.SphereMesh(self.ctx, program, basic, radius= .5, fragments=16)
        mesh_arr = [sphere1, sphere1, sphere1, sphere1,sphere1, sphere1 ]
        
        
        
        self.scene.add_mesh_arr(mesh_arr)
        self.scene.update_camera_specs([0, 0, 2])
        
        
        
    def createSolorScene(self, numAsteroids):
        """
        Creates a scene for the solar system with a numeber of asteroids.

        Parameters
        ----------
        numAsteroids : int
            The number of asteroids to add to the scene.

        Returns
        -------
        None.

        """
        
        # Grabbing the mouse for camera control.
        pg.event.set_grab(True)     
        
        
        # Planet properties
        planet_shine = 5.0
        planet_specular = .5
        planet_ambient = .3
        
        
        
        self.scene.backround_color = [0, 0, 0]
        self.scene.camera.mouse_sens = .4
        

        
        # Creating the textures
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
        
        
        
        # Creating the planet shaders.
        
        planet_shader = shaderProgram.ShaderProgram(self.ctx, 'planet').program
        sun_shader = shaderProgram.ShaderProgram(self.ctx, 'sun').program
        skybox_shader = shaderProgram.ShaderProgram(self.ctx, 'skybox').program
        
        
        # Creating the skybox object.
        sky_box = skybox.SkyBox(self.ctx, 'skybox', skybox_shader)
        self.scene.add_skybox(sky_box)
        
        # Creating the mesh objects.
        sun = mesh.Sphere(self.ctx, sun_shader, sun_text, 
                              radius = .1, fragments = 40)
        mercury = mesh.Sphere(self.ctx, planet_shader, mercury_text, 
                                  radius = .01, fragments=32)
        venus = mesh.Sphere(self.ctx, planet_shader, venus_text, 
                                radius = .03, fragments = 32)
        earth = mesh.Sphere(self.ctx, planet_shader, earth_text, 
                                radius = .03, fragments = 32)
        mars = mesh.Sphere(self.ctx, planet_shader, mars_text, 
                                radius = .025, fragments = 32)
        jupiter = mesh.Sphere(self.ctx, planet_shader, jupiter_text, 
                                radius = .06, fragments = 35)
        comet = mesh.Sphere(self.ctx, planet_shader, comet_text, 
                                radius = .005, fragments = 32)
        asteroid = mesh.Sphere(self.ctx, planet_shader, asteroid_text, 
                                radius = .005, fragments = 32)
        
        
        
        # Adding planets and comet to the scene 
        mesh_arr = [sun, mercury, venus, earth, mars, jupiter, comet]
        
        # Duping the asteroids
        for i in range(numAsteroids):   
            mesh_arr.append(asteroid)
            
            
        # adding asteroids and light.    
        self.scene.add_mesh_arr(mesh_arr)
        self.scene.add_light([0,0,0], [1, 1, 1])
        
        # updating camera
        self.scene.update_camera_specs([1, 0, 0])
        self.scene.camera.velocity = 0.0005 / self.render_speed
        
    
        

    def render(self, dt):  
        """
        Renders scene

        Parameters
        ----------
        dt : float
            Chnage in time since last frame.

        Returns
        -------
        None.

        """
        
        self.ctx.clear(self.scene.backround_color[0], 
                       self.scene.backround_color[1],
                       self.scene.backround_color[2])
        
        self.scene.render(dt, self.model.phobjects[:, :])
        
        self.model.advance(dt)
          
        
        pg.display.flip()
            
    def destroy(self):
        """
        Garbage collection

        Returns
        -------
        None.

        """
        self.scene.destroy()
