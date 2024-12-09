#include "camera.h"

static float lastX = 0, lastY = 0;
static bool isDragging = false;

Camera camera = {
    {1000.0f, 100.0f, 1000.0f},
    {0.0f, 0.0f, -1.0f},
    {0.0f, 1.0f, 0.0f},
    {0.0f, 0.0f, 0.0f},
    {0.0f, 1.0f, 0.0f},
    -120.0f,
    0.0f,
    2.5f,
    0.5f,
    45.0f
};

void updateCamera()
{
    vec3 front;
    front[0] = cos(glm_rad(camera.yaw)) * cos(glm_rad(camera.pitch));
    front[1] = sin(glm_rad(camera.pitch));
    front[2] = sin(glm_rad(camera.yaw)) * cos(glm_rad(camera.pitch));
    glm_vec3_normalize_to(front, camera.front);

    glm_vec3_cross(camera.front, camera.worldUp, camera.right);
    glm_vec3_cross(camera.right, camera.front, camera.up);
}

void processKeyboardInput(GLFWwindow *window, float deltaTime) {
    // float velocity = camera.speed * deltaTime;
    float velocity = 10.0f;
    vec3 vel_scale;
    
    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) {
        glm_vec3_scale(camera.front, velocity, vel_scale);
        glm_vec3_add(camera.position, vel_scale, camera.position);
    }
    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS) {
        glm_vec3_scale(camera.front, velocity, vel_scale);
        glm_vec3_sub(camera.position, vel_scale, camera.position);
    }
    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS) {
        glm_vec3_scale(camera.right, velocity, vel_scale);
        glm_vec3_sub(camera.position, vel_scale, camera.position);
    }
    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS) {
        glm_vec3_scale(camera.right, velocity, vel_scale);
        glm_vec3_add(camera.position, vel_scale, camera.position);
    }
}

void mouseButtonCallback(GLFWwindow* window, int button, int action, int mods)
{
    if (button == GLFW_MOUSE_BUTTON_LEFT) {
        if (action == GLFW_PRESS) {
            isDragging = true;
        }
        else if (action == GLFW_RELEASE) {
            isDragging = false;
        }
    }
}

void mouseCallback(GLFWwindow* window, double xpos, double ypos)
{
    if (isDragging == false) {
        lastX = xpos;
        lastY = ypos;
        return;
    }

    float xoffset = xpos - lastX;
    float yoffset = lastY - ypos;
    // printf("%f %f", xoffset, yoffset);
    lastX = xpos;
    lastY = ypos;

    xoffset *= camera.sensitivity;
    yoffset *= camera.sensitivity;

    camera.yaw += xoffset;
    camera.pitch += yoffset;

    if (camera.pitch > 89.0f) camera.pitch = 89.0f;
    if (camera.pitch < -89.0f) camera.pitch = -89.0f;

    updateCamera();
    printf("pitch: %f, yaw: %f\n", camera.pitch, camera.yaw);
    printf("x: %f, y: %f, z: %f\n", camera.position[0], camera.position[1], camera.position[2]);
}

void scrollCallback(GLFWwindow* window, double xoffset, double yoffset) {
    camera.zoom -= (float)yoffset;
    if (camera.zoom < 1.0f) camera.zoom = 1.0f;
    if (camera.zoom > 180.0f) camera.zoom = 45.0f;
}
