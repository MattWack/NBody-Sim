#version 300 es
precision highp float;

in vec2 uv_0; 

uniform sampler2D u_texture_0;
uniform vec3 ambient;
uniform vec3 mat_color;

out vec4 FragColor;


void main(){
    vec3 color = mat_color*texture(u_texture_0, uv_0).rgb;

    FragColor = vec4(ambient*color, 1.0);
}