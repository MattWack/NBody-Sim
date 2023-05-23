#version 300 es
precision highp float;

in vec3 in_position;
in vec2 in_texcoord_0;


uniform mat4 proj_mat;
uniform mat4 world_mat;
uniform mat4 view_mat;

out vec2 uv_0;

void main(){    
    uv_0 = in_texcoord_0;
    gl_Position = proj_mat * view_mat * world_mat * vec4(in_position, 1.0);
}
