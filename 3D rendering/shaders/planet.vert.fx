#version 300 es
precision highp float;

// Attributes
in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

// Uniforms
// projection 3D to 2D
uniform mat4 world_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

// Output
out vec3 model_normal;
out vec4 FragPos;
out vec2 model_uv;

void main() {
    // Pass vertex normal onto the fragment shader
    mat3 normTransform = inverse(transpose(mat3(world_mat)));

    model_normal = normTransform*in_normal;

    // Pass vertex texcoord onto the fragment shader
    model_uv = in_texcoord_0;
    FragPos = world_mat * vec4(in_position, 1.0);
    // Transform and project vertex from 3D world-space to 2D screen-space
    gl_Position = proj_mat * view_mat * world_mat * vec4(in_position, 1.0);
}
