
#ifndef SHADER_H
#define SHADER_H

#include <GLFW/glfw3.h>
#include <stdio.h>
#include <stdlib.h>
#include "camera.h"

void getDegreeOrderHarmonic(int* L, int* M, size_t sh_count);

float sigmoid(float x);
unsigned char normalizeToColor(float value);

#endif
