#version 300 es
precision highp float;

// Attributes
in vec3 in_position;


// Uniforms
// projection 3D to 2D
uniform mat4 view_mat;
uniform mat4 proj_mat;

// Output
out vec3 FragPos;


void main(){
    FragPos = in_position;
    vec4 pos = proj_mat * view_mat * vec4(in_position, 1.0);
    gl_Position = pos.xyww;
    gl_Position.z -= .00001;

}