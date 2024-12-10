#version 430 core

// Inputs
layout (location = 0) in vec3 aPos;  // Vertex position
layout (std430, binding = 0) buffer splatPosition {
    vec4 positions[];
};
layout (std430, binding = 1) buffer splatScale {
    vec4 scales[];
};
layout (std430, binding = 2) buffer splatColor {
    vec4 colors[];
};
layout (std430, binding = 3) buffer splatQuat {
    vec4 quats[];
};
layout (std430, binding = 4) buffer splatAlpha {
    float alphas[];
};

uniform mat4 model, view, projection;
uniform int shCount;

// Outputs
out vec3 color;
out vec3 instanceScale; 
out mat3 instanceRotation;
out vec3 WorldNormal;
out vec3 WorldPos;

mat3 quatToMat(vec4 q) {
    return mat3(2.0 * (q.x * q.x + q.y * q.y) - 1.0, 2.0 * (q.y * q.z + q.x * q.w), 2.0 * (q.y * q.w - q.x * q.z), // 1st column
                2.0 * (q.y * q.z - q.x * q.w), 2.0 * (q.x * q.x + q.z * q.z) - 1.0, 2.0 * (q.z * q.w + q.x * q.y), // 2nd column
                2.0 * (q.y * q.w + q.x * q.z), 2.0 * (q.z * q.w - q.x * q.y), 2.0 * (q.x * q.x + q.w * q.w) - 1.0); // last column
}

mat4 translate(mat4 model, vec3 t) {
    mat4 translation = mat4(1.0f);  // Start with identity matrix
    translation[3] = vec4(t, 1.0f); // Set translation values in the last column
    return model * translation;      // Multiply the model matrix by the translation matrix
}

void main() {
    vec3 position = vec3(positions[gl_InstanceID]);
    vec3 scale = vec3(scales[gl_InstanceID]);
    mat3 rot = quatToMat(quats[gl_InstanceID]);  // Function to convert quaternion to rotation matrix

    vec3 spherePos = normalize(aPos);
    // vec3 worldPosition = spherePos * scale * rot + position; // splats -> must be fragement rendered to be a sphere
    vec3 worldPosition = spherePos + position; // points -> ready to render

    WorldPos = worldPosition;
    WorldNormal = normalize(worldPosition);
    instanceRotation = rot;
    instanceScale = scale;

    gl_Position = projection * view * model * vec4(worldPosition, 1.0f);
    // color = vec3(colors[gl_InstanceID]) * alpha + vec3(0.5);
    color = vec3(1.0f); // white
}
