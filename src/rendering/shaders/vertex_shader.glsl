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

// Outputs
out vec3 position;
out vec3 ellipsoidCenter;
out vec3 ellipsoidScale;
out mat3 ellipsoidRot;
out float ellipsoidAlpha;
out vec3 color;
out mat4 model_t;

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
    // mat4 model_t = translate(model, vec3(positions[gl_InstanceID]));
    // #1: Scale the input vertices
    vec3 scale = vec3(scales[gl_InstanceID]);
    vec3 scaled = aPos * scale;

    // #2: Transform the quaternions into rotation matrices
    mat3 rot = quatToMat(quats[gl_InstanceID]);  // Function to convert quaternion to rotation matrix
    vec3 rotated = rot * scaled;

    // #3: Translate the vertices
    vec3 posOffset = rotated + vec3(positions[gl_InstanceID]);  // Using position as the translation
    vec4 mPos = vec4(posOffset, 1.0);  // Final model position in homogeneous coordinates

    // #4: Pass the ellipsoid parameters to the fragment shader
    position = vec3(mPos);
    ellipsoidCenter = vec3(positions[gl_InstanceID]);
    ellipsoidScale = scale;
    ellipsoidRot = rot;
    ellipsoidAlpha = alphas[gl_InstanceID];

    gl_Position = projection * view * model * mPos;
    color = vec3(colors[gl_InstanceID]) * vec3(ellipsoidAlpha) + vec3(0.5);
}
