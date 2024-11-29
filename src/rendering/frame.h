#ifndef FRAME_H
#define FRAME_H

#include <GLFW/glfw3.h>
#include <cglm/cglm.h>
#include "data.h"

extern GLuint _FBO, _RBO, _TEXTURE;

void setupFrame(int width, int height);

#endif
