#ifndef SHADER_H
#define SHADER_H

#include <GLFW/glfw3.h>
#include <stdio.h>
#include <stdlib.h>
#include "camera.h"

GLuint compileShader(GLenum shaderType, const char* shaderSource);
GLuint createShaderProgram();
char* loadShaderSource(const char* filename);
void setupShaderProgram(GLuint shaderProgram, mat4 model, mat4 projection);
void updateShaderProgram(GLuint shaderProgram);

#endif
