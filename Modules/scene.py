# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:50:46 2023

@author: mattw
"""
import light
import camera
import glm
class Scene:
    '''
    Class the manages all the objects in the scene.
    ----------
    ctx : ModerGl.Context
        The current context.
    win_size : list
        The window size
    meshes : list of Mesh
        The list of the all the meshes to be rendered.
    skybox : Skybox
        The skybox object to render
    camera : Camera
        The camera in the scene.
    backround color : list
        The color of the backround.
    
    '''
    
    def __init__(self, ctx, win_size, backround_color = [.2, .2, .2]):
        self.ctx = ctx 
        self.win_size = win_size # Probably want to refactor remove this as an attribute.
        self.meshes = [] # Add two lists, one render mesh, another non-render mesh list so spawning objects can be added.
        self.skybox = None 
        self.camera = camera.Camera(ctx, win_size, [0, 0, 0])
        self.backround_color =  backround_color #RGB
        

    def add_skybox(self, skybox):
        """
        Method that adds the skybox to the scene.

        Parameters
        ----------
        skybox : Skybox
            SkyBox object to add to the scene.

        Returns
        -------
        None.

        """
        self.skybox = skybox
        skybox.program['proj_mat'].write(self.camera.get_proj_mat())
        
    def add_mesh_arr(self, mesh_arr):
        """
        Method that appends an array of meshes to the meshes property.

        Parameters
        ----------
        mesh_arr : list of Mesh
            The list of meshes to add.

        Returns
        -------
        None.

        """
        for mesh in mesh_arr:
            mesh.program['proj_mat'].write(self.camera.get_proj_mat())
            self.meshes.append(mesh)
        
            
    def add_light(self, light_pos, light_color):
        """
        Method to add a light to the scene.

        Parameters
        ----------
        light_pos : list
            The postion of the light in world space.
        light_color : list
            The color of the light.

        Returns
        -------
        None.

        """
        self.light = light.Light(light_pos, light_color) 
        
    def update_camera_specs(self, in_pos, fov=60.0, near=.1, far=100.0, yaw=-90, pitch=0):
        """
        Method that updates the camera.

        Parameters
        ----------
        in_pos : list
            The initail positon of the camera.
        fov : float, optional
            The field of view of the camera. The default is 60.0.
        near : float, optional
            The near clipping plane of the camera The default is .1.
        far : float, optional
            The far clipping plane of the camera. The default is 100.0.
        yaw : float, optional
            The yaw angle of the camera. The default is -90.
        pitch : flaot, optional
            The pitch angle of the camera. The default is 0.

        Returns
        -------
        None.

        """
        mounted_idx = self.camera.mounted_phobject_index
        self.camera = camera.Camera(self.ctx, self.win_size, in_pos, fov=fov, 
                                    near=near, far=far, yaw=yaw, pitch=pitch)
        self.camera.mounted_phobject_index = mounted_idx
        
        if len(self.meshes) != 0:
            for mesh in self.meshes:
                mesh.program['proj_mat'].write(self.camera.get_proj_mat())
        
        self.skybox.program['proj_mat'].write(self.camera.get_proj_mat())
                
        
        
    def destroy(self):
        """
        Garbage collection

        Returns
        -------
        None.

        """
        [mesh.destroy() for mesh in self.meshes]
        
        
            
        
    
    def render(self, dt, phobject_mat):
        """
        Renders the meshes, light, and skybox in the scene

        Parameters
        ----------
        dt : float
            Change in time from last frame.
        phobject_mat : ndarray
            The portion of the phobject matrix that holds the phobject info.
            
        Returns
        -------
        None.

        """
        

        self.camera.update(dt, phobject_mat)
        
        # Changing the postion of the light to the suns.
        self.light.pos = phobject_mat[0, 0:3]        
    
        
    
        ### Probably one of the largest bottlenecks, if someone finds a way to run the shaders 
        ### without using a python loop then the number of renderable objects will increase.
        for i, mesh in enumerate(self.meshes):
            
            
            mesh.update_mesh_state(phobject_mat[i, :3])
            mesh.program['view_mat'].write(self.camera.get_view_mat())
            
            # The Sun shader does not use these, so this is my dirty solution (I am sorry)
            if i > 0: 
                mesh.program['camera_position'].write(self.camera.position)
                
                mesh.program['light_position'].value = glm.vec3(self.light.pos)
                mesh.program['light_color'].value = glm.vec3(self.light.color)
            mesh.render()
            
            if self.skybox:
                self.skybox.program['view_mat'].write(glm.mat4(glm.mat3(self.camera.get_view_mat())))
                self.skybox.render()
            
        
    
    
     
    
            
            
        