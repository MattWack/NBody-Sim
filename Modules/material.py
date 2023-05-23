# -*- coding: utf-8 -*-
"""
Created on Thu May 11 19:16:12 2023

@author: mattw
"""
import pygame as pg
import os

class Material():
    '''
    ----------
    ctx : ModerGl.Context
        The current modernGl context
    text_file : string
        The name of the texture file to bind to the material (needs to be in the texture folder)
    mat_color : list of floats
        The RGB values of the material, needs to normalized to 1.0
    ambient : float
        The ambient brightness of the material, range of 0.0 - 1.0
    mat_specular : float
        The specular value of the material, range of 0.0 - 1.0
    mat_shininess : float
        The shine of the material
        
    
    '''
    
    
    def __init__(self, ctx, text_file, mat_color, rot = 0, 
                 ambient=None, mat_specular=None, mat_shininess=None):
        """
        

        Parameters
        ----------
        rot : float, optional
            How much to rotate the texture by.

        Returns
        -------
        None.

        """
        
        self.ctx = ctx
        self.texture = self._get_texture(text_file, rot)
        self.mat_color = mat_color
        self.ambient = ambient
        self.mat_specular = mat_specular
        self.mat_shininess = mat_shininess
            
            
    def _get_texture(self, text_file, rot):
        """
        Helper method to get the ModernGl.Texture object from an image.

        Parameters
        ----------
        text_file : string
            The name of the texture file to bind to the material (needs to be in the texture folder)
        rot : float, optional
            How much to rotate the texture by.

        Returns
        -------
        texture : ModernGl.Texture
            The texture object.

        """
        cwd = os.getcwd()
        texture = pg.image.load(cwd + "/textures/" + text_file)
        texture = pg.transform.rotate(texture, rot)
        texture = self.ctx.texture(size=texture.get_size(), components = 3,
                                   data=pg.image.tostring(texture, 'RGB'))
        
        return texture
    
            