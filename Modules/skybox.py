# -*- coding: utf-8 -*-
"""
Created on Wed May 17 16:13:44 2023

@author: mattw
"""
import pygame as pg
import moderngl_window as mglw 
import os
class SkyBox():
    '''Class for camera in a 3D scene
    ----------
    ctx: ModernGl.Context
        The context where to put the skybox
    program: ModernGl.Program
        The shader program to calculate the shading of the skybox
    texture: ModernGl.Texture
        The cube texture to bind the to skybox.
    voa: ModernGl.VOA
        The vertex object array for the skybox.
    
    
    '''
    def __init__(self, ctx, file_name, program):
        """
        

        Parameters
        ----------

        file_name : string
            The filename of the 6 textures to map to the skybox (needs to be in texture folder).

        Returns
        -------
        None.

        """
        self.ctx = ctx
        self.program = program 
        self.textures = self._get_textures(file_name)
        self.voa = mglw.geometry.cube(normals = False, uvs = False)
        
    
    def _get_textures(self, file_name):
        """
        Helper method to create the textues from a given filename

        Parameters
        ----------
        file_name : string
            The filename of the 6 textures to map to the skybox (needs to be in texture folder).

        Returns
        -------
        texture_cube : ModernGl.Texture_cube
            The texture cube that is used as the skybox.

        """
        cwd = os.getcwd()
        
        faces = ['_right', '_left', '_top', '_bottom', '_front', '_back']
        textures = []
        for face in faces:
            texture = pg.image.load(cwd + '/textures/' + file_name + f'{face}.png').convert()
            texture = pg.transform.rotate(texture, 0)
            textures.append(texture)
                
        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size = size, components = 3, data = None)
        
        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data = texture_data)
            
        return texture_cube
    
    
    def render(self):
        """
        Renders the skybox

        Returns
        -------
        None.

        """
        self.textures.use(0)
        self.program['u_texture_skybox'].value = 0
        self.voa.render(self.program)
        
        
    

        
    
        