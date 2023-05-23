# -*- coding: utf-8 -*-
"""
Created on Thu May 11 19:16:12 2023

@author: mattw
"""
import pygame as pg
import os

class Material():
    
    def __init__(self, ctx, text_file, mat_color, xflip = False, yflip = True, 
                 ambient=None, mat_specular=None, mat_shininess=None):
        
        self.ctx = ctx
        self.texture = self._get_texture(text_file, xflip, yflip)
        self.mat_color = mat_color
        self.ambient = ambient
        self.mat_specular = mat_specular
        self.mat_shininess = mat_shininess
            
            
    def _get_texture(self, text_file, xflip, yflip):
        cwd = os.getcwd()
        texture = pg.image.load(cwd + "/textures/" + text_file)
        texture = pg.transform.flip(texture, xflip, yflip)
        texture = self.ctx.texture(size=texture.get_size(), components = 3,
                                   data=pg.image.tostring(texture, 'RGB'))
    
        return texture
    
            