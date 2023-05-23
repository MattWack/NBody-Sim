#version 300 es
precision highp float;

in vec2 uv_0; 

uniform sampler2D u_texture_0;

out vec4 FragColor;


void main(){
    vec3 color = texture(u_texture_0, uv_0).rgb;

    FragColor = vec4(color, 1.0);
}