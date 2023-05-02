# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 13:44:06 2023

@author: mattw
"""
import numpy as np
import pygame as pg
class Render():
    '''Class to render an animation
    ----------
    scale : 2-array of floats
        An array to scale the model given by [sx, sy]
    offset : 2-array of ints
        An array to offset the model given by [ox, oy]
        
    '''
    
    def __init__(self, scale, offset):
        self.scale = scale
        self.offset = offset
        pg.init()
        
    
    def render(self, model):
        """
        Renders the model and draws new coords.

        Parameters
        ----------
        model : Model
            The physics model to render.

        Returns
        -------
        new_coords : 
            DESCRIPTION.

        """
        new_coords = np.zeros((len(model.phobject), 2))
        
        for i, obj in enumerate(model.phobject):
            coord = [obj.pos.x, obj.pos.y]
            new_coords[i, :] = self._coord_transform(coord)
        
        return new_coords
        
            
    def _coord_transform(self, coord):
        """
        Helper function to take in coordinates and return new coords with the 
        scale and offset.

        Parameters
        ----------
        coord : 1x2 array of flaots
            Array of coords given by [x, y].

        Returns
        -------
        1x2 array of int
            The new transformed coords.

        """
        a = np.dot([[self.scale[0], 0], [0, -self.scale[1]]], np.asarray([coord]).T)
        a = np.add(a.T, np.asarray(self.offset))
        return a
    
    def open_display(self, screen_size):
        """
        Method that opens the window to aniamte on.

        Parameters
        ----------
        screen_size : 2d-array of int
            The array for the screen size given by [width, height].

        Returns
        -------
        None.

        """
        self.screen = pg.display.set_mode(screen_size)
        
    
class SolarRender(Render):
    '''Render for the solar system model
    ----------
    colors : array of rbg values
        An array of the colors to animate each object in the model
    sizes : array of int
        An array of the sizes for the radii of the objects
    scale : optional 2d array of int
        The scaling factor for render, [150, 150] as default.
    offset : optional 2d array of int
        The offset factor for render, [550, 275] as default.
        
    '''
    
    def __init__(self, colors, sizes, scale = [150, 150], offset = [550, 275]):
        self.colors = colors
        self.sizes = sizes
        super().__init__(scale, offset)
        
    def render(self, model):
        """
        Renders the model and draws new coords.

        Parameters
        ----------
        model : Model
            The physics model to render.

        Returns
        -------
        None.

        """
        
        new_coords = np.zeros((len(model.phobject), 2))
        
        for i, phob in enumerate(model.phobject):
            coord = [phob.pos.x, phob.pos.y]
            new_coords[i, :] = self._coord_transform(coord)
            pg.draw.circle(self.screen, 
                           self.colors[i], 
                           new_coords[i, :].astype(int), 
                           self.sizes[i])
            
            
class NBodyRender(Render):
    '''Render for the solar system model
    ----------
    colors : array of rbg values
        An array of the colors to animate each object in the model
    sizes : array of int
        An array of the sizes for the radii of the objects
    scale : optional 2d array of int
        The scaling factor for render, [150, 150] as default.
    offset : optional 2d array of int
        The offset factor for render, [550, 275] as default.
        
    '''
    
    def __init__(self, colors, sizes, scale = [150, 150], offset = [550, 275]):
        self.colors = colors
        self.sizes = sizes
        super().__init__(scale, offset)
        
    def render(self, model):
        """
        Renders the model and draws new coords.

        Parameters
        ----------
        model : Model
            The physics model to render.

        Returns
        -------
        None.

        """
        
        new_coords = np.zeros((np.shape(model.phobject)[0],2))
        
        for i in range(np.shape(model.phobject)[0]):
            coord = [model.phobject[i, 0], model.phobject[i,1]]
            new_coords[i, :] = self._coord_transform(coord)
            pg.draw.circle(self.screen, 
                           self.colors[i], 
                           new_coords[i, :].astype(int), 
                           self.sizes[i])
            
        
        