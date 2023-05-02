# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 13:42:02 2023

@author: mattw
"""
import pygame as pg
import numpy as np
class Animate():
    '''Class to animate a model
    ----------
    model : Model
        The physics model to animate.
    render : Render
        The render for the animation
    screen_size: 2x1 array of int
        The size of the screen given by [width, height]
    time: float
        The time to animate
        
    '''
    
    def __init__(self, model, render, screen_size, time = 0):
        self.model = model
        self.render = render
        self.screen_size = screen_size
        self.done = False
        self.time = time
        
        
    def run(self):
        """
        Method that runs the animation

        Returns
        -------
        None.

        """
        self.render.open_display(self.screen_size)
        
        while not self.done:
            
            dt = self._timing_handler()
            
            self._event_handler()
            
            
            self.render.screen.fill((0,0,0))
            
            self.render.render(self.model)
            
            pg.display.flip()
            
            self.model.advance(dt)
            
            pg.time.delay(10)
            
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
        elapsed_time = (current_time - self.time) / 10000
        self.time = current_time
        return elapsed_time
    
        
    def _event_handler(self):
        """
        Helper method to handle events

        Returns
        -------
        None.

        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done == True
                    
                    
        
            