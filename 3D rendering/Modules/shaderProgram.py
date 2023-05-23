# -*- coding: utf-8 -*-
"""
Created on Thu May 11 11:57:16 2023

@author: mattw
"""
import os


class ShaderProgram():
    
    def __init__(self, ctx, shader_name = 'default'):
        cwd = os.getcwd()
        with open(cwd + "\shaders\{shader_name}.vert.fx".format(shader_name=shader_name)) as file:
            vertex_shader = file.read()

        with open(cwd + "\shaders\{shader_name}.frag.fx".format(shader_name=shader_name)) as file:
            fragment_shader = file.read()

        self.program =  ctx.program(vertex_shader= vertex_shader, 
                                         fragment_shader=fragment_shader)
    