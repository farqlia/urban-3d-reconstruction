#ifndef CAMERA_H
#define CAMERA_H

#include <cglm/cglm.h>
#include <GLFW/glfw3.h>
#include "data.h"
#include "math.h"

// Struct to represent the camera
typedef struct {
    vec3 position;
    vec3 front;
    vec3 up;
    vec3 right;
    vec3 worldUp;
    float yaw;
    float pitch;
    float speed;
    float sensitivity;
    float zoom;
} Camera;

extern Camera camera;

void updateCamera();
void processKeyboardInput(GLFWwindow *window, float deltaTime);
void mouseButtonCallback(GLFWwindow* window, int button, int action, int mods);
void mouseCallback(GLFWwindow* window, double xpos, double ypos);
void scrollCallback(GLFWwindow* window, double xoffset, double yoffset);

#endif
