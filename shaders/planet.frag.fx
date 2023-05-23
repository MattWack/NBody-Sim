#version 300 es
precision mediump float;

// Input
in vec3 model_normal;
in vec4 FragPos;
in vec2 model_uv;

// Uniforms
// material
uniform vec3 mat_color;
uniform vec3 mat_specular;
uniform float mat_shininess;
uniform sampler2D u_texture_0;
// camera
uniform vec3 camera_position;
// lights
uniform vec3 ambient; // Ia

uniform vec3 light_position;
uniform vec3 light_color; // Ip 

// Output
out vec4 FragColor;

void main() {
    // Color
    // vec3 mat_color = light_colors * mat_color;
    vec3 n = normalize(model_normal);

    vec3 illum_a = ambient;

    vec3 v = normalize(camera_position - FragPos.xyz);

    
    vec3 l = normalize(light_position - FragPos.xyz);
    vec3 illum_b = light_color * max(dot(n, l), 0.0);

    vec3 r = normalize(reflect(-l, n));
    vec3 illum_s = light_color * mat_specular * pow(max((dot(r, v)), 0.0) , mat_shininess);


   

    // FragColor = vec4(mat_color * texture(mat_texture, model_uv).rgb, 1.0);

    FragColor = vec4((illum_a + illum_b)* mat_color * texture(u_texture_0, model_uv).rgb + illum_s, 1.0);
}
