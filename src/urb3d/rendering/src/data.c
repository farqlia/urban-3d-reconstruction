#include "data.h"

vec4* _positions;
vec4* _scales;
vec4* _colors;
vec4* _quaternitions;
float* _alphas;
GLuint _VAO, _VBO;
GLuint _positionSSBO, _scaleSSBO, _colorSSBO, _quatSSBO, _alphaSSBO;

float CUBE[] = {
    // Back
    -1.0f, -1.0f, -1.0f,
    1.0f, -1.0f, -1.0f,
    1.0f, 1.0f, -1.0f,
    1.0f, 1.0f, -1.0f,
    -1.0f, 1.0f, -1.0f,
    -1.0f, -1.0f, -1.0f,

    // Front
    -1.0f, -1.0f, 1.0f,
    1.0f, -1.0f, 1.0f,
    1.0f, 1.0f, 1.0f,
    1.0f, 1.0f, 1.0f,
    -1.0f, 1.0f, 1.0f,
    -1.0f, -1.0f, 1.0f,

    // Bottom
    -1.0f, -1.0f, -1.0f,
    1.0f, -1.0f, -1.0f,
    1.0f, -1.0f, 1.0f,
    1.0f, -1.0f, 1.0f,
    -1.0f, -1.0f, 1.0f,
    -1.0f, -1.0f, -1.0f,

    // Top
    -1.0f, 1.0f, -1.0f,
    1.0f, 1.0f, -1.0f,
    1.0f, 1.0f, 1.0f,
    1.0f, 1.0f, 1.0f,
    -1.0f, 1.0f, 1.0f,
    -1.0f, 1.0f, -1.0f,

    // Left
    -1.0f, -1.0f, -1.0f,
    -1.0f, 1.0f, -1.0f,
    -1.0f, 1.0f, 1.0f,
    -1.0f, 1.0f, 1.0f,
    -1.0f, -1.0f, 1.0f,
    -1.0f, -1.0f, -1.0f,

    // Right
    1.0f, -1.0f, -1.0f,
    1.0f, 1.0f, -1.0f,
    1.0f, 1.0f, 1.0f,
    1.0f, 1.0f, 1.0f,
    1.0f, -1.0f, 1.0f,
    1.0f, -1.0f, -1.0f,
};

void generateStructureOfArrays(PointCloudData* data, size_t pointCount)
{
    _positions = malloc(pointCount * sizeof(vec4));
    _scales = malloc(pointCount * sizeof(vec4));
    _colors = malloc(pointCount * sizeof(vec4));
    _quaternitions = malloc(pointCount * sizeof(vec4));
    _alphas = malloc(pointCount * sizeof(float));

    for (size_t i = 0; i < pointCount; i++) {
        PointCloudData* splat = &data[i];

        vec4* pos = &_positions[i];
        vec3 xyz;
        xyz[0] = splat->position[0];
        xyz[1] = -1.0f * splat->position[2];
        xyz[2] = splat->position[1];
        glm_vec4(xyz, 1.0f, *pos);

        const double MULTIPLIER = 1000.0f;
        vec4 mul = {MULTIPLIER, MULTIPLIER, MULTIPLIER, MULTIPLIER};
        glm_vec4_mul(*pos, mul, *pos);

        vec4* scale = &_scales[i];
        glm_vec4(splat->scalars, 1.0f, *scale);

        vec4* color = &_colors[i];
        if (splat->sh != NULL) {
            float avgShX = 0.0f;
            float avgShY = 0.0f;
            float avgShZ = 0.0f;
            for (size_t j = 0; j < splat->sh_count * 3; j++) {
               avgShX += splat->sh[j++] * splat->a;
               avgShY += splat->sh[j++] * splat->a;
               avgShZ += splat->sh[j++] * splat->a;
            }
            vec3 avgs = { avgShX * 255, avgShY * 255, avgShZ * 255 };
            glm_vec4(avgs, 1.0f, *color);
        } else
            glm_vec4(splat->color, 1.0f, *color);

        vec4* quaternitions = &_quaternitions[i];
        glm_vec4_copy(splat->quaternition, *quaternitions);

        glm_vec4_normalize(*quaternitions);

        _alphas[i] = (1.0f / (1.0f + exp(splat->a * -1.0f)));
    }
}

void generateSSBO(PointCloudData* data, size_t pointCount)
{
    GLuint r_pos = GL_NONE;
    glCreateBuffers(1, &r_pos);
    glNamedBufferStorage(r_pos, sizeof(vec4) * pointCount, _positions, GL_MAP_READ_BIT);

    _positionSSBO = r_pos;

    GLuint r_scale = GL_NONE;
    glCreateBuffers(1, &r_scale);
    glNamedBufferStorage(r_scale, sizeof(vec4) * pointCount, _scales, GL_MAP_READ_BIT);

    _scaleSSBO = r_scale;

    GLuint r_color = GL_NONE;
    glCreateBuffers(1, &r_color);
    glNamedBufferStorage(r_color, sizeof(vec4) * pointCount, _colors, GL_MAP_READ_BIT);

    _colorSSBO = r_color;

    GLuint r_quat = GL_NONE;
    glCreateBuffers(1, &r_quat);
    glNamedBufferStorage(r_quat, sizeof(vec4) * pointCount, _quaternitions, GL_MAP_READ_BIT);

    _quatSSBO = r_quat;

    GLuint r_alpha = GL_NONE;
    glCreateBuffers(1, &r_alpha);
    glNamedBufferStorage(r_alpha, sizeof(float) * pointCount, _alphas, GL_MAP_READ_BIT);

    _alphaSSBO = r_alpha;

    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, _positionSSBO);
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, _scaleSSBO);
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, _colorSSBO);
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, _quatSSBO);
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, _alphaSSBO);
}

void generateVAOVBO(PointCloudData* data, size_t pointCount)
{
    glGenVertexArrays(1, &_VAO);
    glGenBuffers(1, &_VBO);

    glBindVertexArray(_VAO);
    glBindBuffer(GL_ARRAY_BUFFER, _VBO);

    // glBufferData(GL_ARRAY_BUFFER, 108 * sizeof(float), CUBE, GL_STATIC_DRAW);
    // Setting CUBE as model to render (location = 0)
    glBufferData(GL_ARRAY_BUFFER, sizeof(CUBE), CUBE, GL_STATIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);
}