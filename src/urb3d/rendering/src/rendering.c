#include "rendering.h"

void render(size_t pointCount)
{
    glBindVertexArray(_VAO);
    glDrawArraysInstanced(GL_TRIANGLES, 0, 36, pointCount);
    glBindVertexArray(0);
}