# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:24:08 2023

@author: mattw
"""
import pygame as pg

class Animate():
    


    def __init__(self, model, render, render_speed= 1/1000, time = 0):
        self.model = model
        self.render = render
        self.done = False
        self.time = time
        self.render_speed = render_speed
        
    def run(self):
        """
        Method that runs the animation

        Returns
        -------
        None.

        """
        
        while not self.done:
            
            dt = self._timing_handler()
            
            self._event_handler()
            
            self.render.render(dt)
            
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
        elapsed_time = (current_time - self.time) * self.render_speed
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
                    self.done = True
                    
                    