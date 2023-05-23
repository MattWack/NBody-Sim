# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:50:54 2023

@author: mattw
"""
import moderngl_window as mdgw
import numpy as np
import glm

class Mesh():
    '''
    ----------
    ctx : ModernGl.Context
        The current modernGl context
    program : ModernGl.Program
        The shader program to render the mesh.
    material : Material
        A Material object for the mesh
    world_mat : glm.Matrix4 
        The world martix
    
    '''
    
    def __init__(self, ctx, program, material, in_pos=[0.0, 0.0, 0.0]):
        """
        

        Parameters
        ----------

        in_pos : list, optional
            The initial position in world space. The default is [0.0, 0.0, 0.0].

        Returns
        -------
        None.

        """
        self.ctx = ctx
        self.program = program
        self.material = material
        self.update_mesh_state(pos=in_pos)
        self.apply_properties()
        
        
    def update_mesh_state(self, pos=[0, 0, 0], rot =[0, 0, 0], scaling=[1, 1, 1]):
        """
        Updates the state of the mesh in world space.

        Parameters
        ----------
        pos : list, optional
            The position of the mesh. The default is [0, 0, 0].
        rot : list, optional
            The rotation of the mesh. The default is [0, 0, 0].
        scaling : list, optional
            The scaling of the mesh. The default is [1, 1, 1].

        Returns
        -------
        None.

        """
    
        translate = glm.mat4(np.array([[1, 0, 0, pos[0]],
                                       [0, 1, 0, pos[1]],
                                       [0, 0, 1, pos[2]],
                                       [0, 0, 0, 1]]))
        rot = glm.mat4() #Implment if you want to see planets rotate
        scaling = glm.scale(scaling) 
                           
        self.world_mat = glm.mul(translate, scaling)
        
    def render(self):
        """
        Renders the mesh

        Returns
        -------
        None.

        """
        self.program['world_mat'].write(self.world_mat)
        self.material.texture.use()
        self.voa.render(self.program)        
        
    def destroy(self):
        """
        Garbage collection

        Returns
        -------
        None.

        """
        self.voa.release()
        self.material.texture.release()
        self.program.release()


    def apply_properties(self):
        """
        Sends the material properties of the mesh to the shader program.

        Returns
        -------
        None.

        """
        
        self.program['mat_color'].value = glm.vec3(self.material.mat_color)
        
        self.program['u_texture_0'].value = 0
        if self.material.ambient:
            self.program['ambient'].value = glm.vec3(self.material.ambient)
        if self.material.mat_specular:
            self.program['mat_specular'].value = glm.vec3(self.material.mat_specular)
        if self.material.mat_shininess:
            self.program['mat_shininess'].value = self.material.mat_shininess

    
    
class Sphere(Mesh):
    '''
    Sphere mesh object.
    ----------
    voa : ModernGl.VOA
        The vertex object array that holds the vertices and other data of a sphere.
    
    '''
    
    def __init__(self, ctx, program, material, in_pos=[0.0, 0.0, 0.0], radius=1.0, fragments=16):
        """
        

        Parameters
        ----------
        in_pos : list, optional
            The initial position in world space. The default is [0.0, 0.0, 0.0].
        radius : float, optional
            The radius of the sphere. The default is 1.0.
        fragments : int, optional
            How many fragments to divide the sphere into. The default is 16.

        Returns
        -------
        None.

        """
        
        
        self.voa = self._create_voa(radius, fragments)
        super().__init__(ctx, program, material, in_pos = in_pos)
        
        
    def _create_voa(self, r, f):
        """
        Helper method to create the voa.

        """
        
        ## This code generates the following name for the attributes in shaders ##
        # POSITION = "in_position"
        # NORMAL = "in_normal"
        # TEXCOORD_0 = "in_texcoord_0"
        
        return mdgw.geometry.sphere(radius=r, rings=f, sectors=f)
    
    

        
        
    
    
        
    
        
    
    