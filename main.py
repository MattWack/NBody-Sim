# -*- coding: utf-8 -*-
"""
Created on Thu May 11 17:19:25 2023

@author: mattw
"""

import animate3D
import Model

def main():
    num_asteroids = 200
    render_speed = 1/50000
    
    model= Model.AsteroidModel(numAsteroids=num_asteroids, dt_max=.01)
    model.add_phobject([1, 0, 0, 0, 0, 0, 0])
    
    win_size = (1400,1000)
    
    animate = animate3D.Animate(model, render_speed=render_speed, win_size=win_size)
    animate.render.createSolorScene(num_asteroids)
    
    animate.run()   
    
if __name__ == '__main__':
    main()