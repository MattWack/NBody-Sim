#version 300 es
precision highp float;

in vec3 FragPos;

uniform samplerCube u_texture_skybox;


out vec4 FragColor;


void main(){
    FragColor = texture(u_texture_skybox, FragPos);
}