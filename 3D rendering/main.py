# -*- coding: utf-8 -*-
"""
Created on Thu May 11 17:19:25 2023

@author: mattw
"""


import render3D
import animate3D
import Solver as slv
import Model


num_asteroids = 250
render_speed = 1/50000
rk4 = slv.RK4()
model= Model.AsteroidModel(numAsteroids=num_asteroids, dt_max=.01)
win_size = (1400,1000)

render = render3D.Render3D(model, win_size, render_speed=render_speed)
render.createSolorScene(num_asteroids)
animate = animate3D.Animate(model, render, render_speed=render_speed)

animate.run()   