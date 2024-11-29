#ifndef DATA_H
#define DATA_H

#include <GLFW/glfw3.h>
#include <cglm/cglm.h>
#include "utils.h"

typedef struct {
    vec3 position;   // Position (x, y, z)
    float a;         // Scalar value a
    vec4 quaternition; // Quaternion (q0, q1, q2, q3)
    vec3 scalars;    // Scalars (s0, s1, s2)
    vec3 color;      // Color (only for second type)
    vec3 normal;     // Normal
    float* sh;       // Harmonic values (only for first type)
    size_t sh_count; // Number of harmonic values
} PointCloudData;

extern float CUBE[];

extern vec4* _positions;
extern vec4* _scales;
extern vec4* _colors;
extern vec4* _quaternitions;
extern float* _alphas;

extern GLuint _VAO, _VBO;
extern GLuint _positionSSBO, _scaleSSBO, _colorSSBO, _quatSSBO, _alphaSSBO;

void generateStructureOfArrays(PointCloudData* data, size_t pointCount);
void generateSSBO(PointCloudData* data, size_t pointCount);
void generateVAOVBO(PointCloudData* data, size_t pointCount);

#endif
