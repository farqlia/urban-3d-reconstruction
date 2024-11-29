#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include "shader.h"
#include "loader.h"
#include "camera.h"
#include "data.h"
#include "rendering.h"

#define WIDTH 800
#define HEIGHT 600
#define TARGET_FPS 5
#define TARGET_FRAME_TIME (1.0 / TARGET_FPS)

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}

// Function to initialize the GLFW window
GLFWwindow* initWindow(int width, int height, const char* title)
{
    if (!glfwInit())
    {
        printf("GLFW initialization failed.\n");
        return NULL;
    }

    GLFWwindow* window = glfwCreateWindow(width, height, title, NULL, NULL);
    if (!window)
    {
        printf("GLFW window creation failed.\n");
        glfwTerminate();
        return NULL;
    }

    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    if (glewInit() != GLEW_OK)
    {
        printf("GLEW initialization failed.\n");
        return NULL;
    }

    return window;
}

int main()
{
    GLFWwindow* window = initWindow(800, 600, "OpenGL Cube");
    if (!window)
    {
        printf("GLFW window creation failed.\n");
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL);
    glfwSetMouseButtonCallback(window, mouseButtonCallback);
    glfwSetCursorPosCallback(window, mouseCallback);
    // glfwSetScrollCallback(window, scroll_callback);

    PointCloudData* data;
    size_t pointCount;
    loadPLY("data/tester.ply", &data, &pointCount);
    generateVAOVBO(data, pointCount);
    generateStructureOfArrays(data, pointCount);
    generateSSBO(data, pointCount);

    GLuint shaderProgram = createShaderProgram();

    mat4 model, projection;
    glm_mat4_identity(projection);
    glm_mat4_identity(model);
    // glm_scale_uni(model, 0.1f);
    // glm_scale_uni(projection, 0.1f);
    glm_perspective(glm_rad(45.0f), (float)WIDTH / (float)HEIGHT, 0.1f, 10000.0f, projection);
    setupShaderProgram(shaderProgram, model, projection);

    float lastFrame = 0.0f;
    updateCamera();
    printf("pitch: %f, yaw: %f\n", camera.pitch, camera.yaw);

    while (!glfwWindowShouldClose(window))
    {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);

        float currentFrame = glfwGetTime();
        float deltaTime = currentFrame - lastFrame;
        lastFrame = currentFrame;

        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glEnable(GL_DEPTH_TEST);

        processKeyboardInput(window, deltaTime);

        // glm_perspective(glm_rad(camera.zoom), 1.0f, 0.1f, 100.0f, projection);
        // glm_rotate(model, (float)glfwGetTime(), (vec3){0.5f, 1.0f, 0.0f});

        updateShaderProgram(shaderProgram);

        render(pointCount);

        glfwSwapBuffers(window);
        glfwPollEvents();

        // if (deltaTime < TARGET_FRAME_TIME)
        //     glfwWaitEventsTimeout(TARGET_FRAME_TIME - deltaTime);
    }

    glDeleteVertexArrays(1, &_VAO);
    glDeleteBuffers(1, &_VBO);
    glDeleteBuffers(1, &_positionSSBO);
    glDeleteBuffers(1, &_scaleSSBO);
    glDeleteBuffers(1, &_colorSSBO);
    glDeleteBuffers(1, &_quatSSBO);
    glDeleteBuffers(1, &_alphaSSBO);
    glDeleteProgram(shaderProgram);

    glfwTerminate();
    return 0;
}

// int main(int argc, char const *argv[])
// {
//     PointCloudData* data;
//     size_t pointCount;
//     loadPLY("tester.ply", &data, &pointCount);
//     return 0;
// }
