# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:24:08 2023

@author: mattw
"""
import pygame as pg
import render3D

class Animate():
    '''
    Class that handles the animation of the scene
    ----------
    model : Model
        The physics model to use for rendering
    render : Render3D
        The renderer that handles the drawing and updating of the scene.
    done : bool
        The boolean that handles when the animation finishes.
    time : float
        The current time from when the animation starts.
    render_speed : float
        How fast to render the objects.
    
    '''
    


    def __init__(self, model, render_speed= 1/1000, time = 0, win_size=(800, 600)):
        """

        Parameters
        ----------
        win_size : tuple, optional
            The size of the window. The default is (800, 600).

        Returns
        -------
        None.

        """
        self.model = model
        render = render3D.Render3D(model, win_size, render_speed=render_speed)
        self.render = render
        self.done = False
        self.time = time
        self.render_speed = render_speed
        
    def run(self):
        """
        Method that runs the animation.

        Returns
        -------
        None.

        """
        
        while not self.done:
            
            dt = self._timing_handler()
            
            self._event_handler()
            
            self.render.render(dt)
            
            pg.time.delay(10)
        
        self.render.destroy()
        pg.quit()
            
            
            
            
    def _timing_handler(self):
        """
        Helper method to handle the change in time between animation frames.

        Returns
        -------
        elapsed_time : flaot
            Time since last frame.

        """
        
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.time) * self.render_speed
        self.time = current_time
        return elapsed_time
    
        
    def _event_handler(self):
        """
        Helper method to handle events. Add conditionals to add features. 

        Returns
        -------
        None.

        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                if event.key == pg.K_1:
                    self.render.scene.camera.mounted_phobject_index = -1
                    self.render.scene.camera.mount_camera(self.render.model.phobjects)
                if event.key == pg.K_2:
                    self.render.scene.camera.mounted_phobject_index = 0
                    self.render.scene.camera.mount_camera_on(self.render.model.phobjects)
                if event.key == pg.K_3:
                    self.render.scene.camera.mounted_phobject_index = 1
                    self.render.scene.camera.mount_camera_on(self.render.model.phobjects)
                if event.key == pg.K_4:
                    self.render.scene.camera.mounted_phobject_index = 2
                    self.render.scene.camera.mount_camera_on(self.render.model.phobjects)
                if event.key == pg.K_5:
                    self.render.scene.camera.mounted_phobject_index = 3
                    self.render.scene.camera.mount_camera_on(self.render.model.phobjects)
                if event.key == pg.K_6:
                    self.render.scene.camera.mounted_phobject_index = 4
                    self.render.scene.camera.mount_camera_on(self.render.model.phobjects)
                if event.key == pg.K_7:
                    self.render.scene.camera.mounted_phobject_index = 5
                    self.render.scene.camera.mount_camera_on(self.render.model.phobjects)
                if event.key == pg.K_8:
                    self.render.scene.camera.mounted_phobject_index = 6
                    self.render.scene.camera.mount_camera_on(self.render.model.phobjects)
                if event.key == pg.K_9:
                    self.render.scene.camera.mounted_phobject_index = 7
                    self.render.scene.camera.mount_camera_on(self.render.model.phobjects)
                if event.key == pg.K_0:
                    self.render.scene.camera.mounted = False
                if event.key == pg.K_p:
                    self.render.model.phobjects[0, -1] = 2 * self.render.model.phobjects[0, -1]
                if event.key == pg.K_z:
                    self.model.reset()
                    
                    
                    
                    