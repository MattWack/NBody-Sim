# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 13:53:11 2023

@author: mattw
"""

import Model
import Render
import Animate
    
def main():
    
   
    solar = Model.NBodySolarModel(dt_max = .003)
    
    colors = [[100, 150, 104],
              [105,105,105], 
              [255, 198, 73],
              [47,106,105],
              [153,61,0],
              [203,218,218]]
    
    sizes = [7, 4, 5, 5, 5, 3]
    render = Render.NBodyRender(colors, sizes,  offset = [400, 300], scale=[100, 100])
    animate = Animate.Animate(solar, render, [800, 600])
    
    animate.run()

    
if __name__ == "__main__":
    main()