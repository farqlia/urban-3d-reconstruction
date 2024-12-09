#if defined(_WIN32)
    #include <windows.h>
    #define GLFW_EXPOSE_NATIVE_WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define GLFW_EXPOSE_NATIVE_X11
    #define EXPORT
#endif

#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <GLFW/glfw3native.h>

#include "shader.h"
#include "loader.h"
#include "camera.h"
#include "data.h"
#include "rendering.h"

#define WIDTH 800
#define HEIGHT 600
#define TARGET_FPS 5
#define TARGET_FRAME_TIME (1.0 / TARGET_FPS)

GLFWwindow* WINDOW = NULL;
PointCloudData* DATA;
size_t DATA_COUNT;
GLuint SHADER_PROGRAM;

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}

// Function to initialize the GLFW window
EXPORT void initWindow()
{
    if (!glfwInit())
    {
        printf("GLFW initialization failed.\n");
        return;
    }

    WINDOW = glfwCreateWindow(WIDTH, HEIGHT, "", NULL, NULL);
    if (!WINDOW)
    {
        printf("GLFW window creation failed.\n");
        glfwTerminate();
        return;
    }

    glfwMakeContextCurrent(WINDOW);
    glfwSetFramebufferSizeCallback(WINDOW, framebuffer_size_callback);

    if (glewInit() != GLEW_OK)
    {
        printf("GLEW initialization failed.\n");
        return;
    }

    glfwSetInputMode(WINDOW, GLFW_CURSOR, GLFW_CURSOR_NORMAL);
    glfwSetMouseButtonCallback(WINDOW, mouseButtonCallback);
    glfwSetCursorPosCallback(WINDOW, mouseCallback);

    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glfwSwapBuffers(WINDOW);
}

EXPORT void loadData(const char* filename)
{
    loadPLY(filename, &DATA, &DATA_COUNT);
    generateVAOVBO(DATA, DATA_COUNT);
    generateStructureOfArrays(DATA, DATA_COUNT);
    generateSSBO(DATA, DATA_COUNT);
}

EXPORT intptr_t getWindowId()
{
    #if defined(_WIN32)
        return (intptr_t)glfwGetWin32Window(WINDOW);
    #elif defined(__linux__)
        #if defined(GLFW_EXPOSE_NATIVE_X11)
            return (intptr_t)glfwGetX11Window(WINDOW);
        #endif
    #endif
}

EXPORT void run()
{
    SHADER_PROGRAM = createShaderProgram();

    mat4 model, projection;
    glm_mat4_identity(projection);
    glm_mat4_identity(model);
    glm_perspective(glm_rad(45.0f), (float)WIDTH / (float)HEIGHT, 0.1f, 10000.0f, projection);
    setupShaderProgram(SHADER_PROGRAM, model, projection);

    float lastFrame = 0.0f;
    updateCamera();

    glEnable(GL_DEPTH_TEST);

    while (!glfwWindowShouldClose(WINDOW))
    {
        if (glfwGetKey(WINDOW, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(WINDOW, true);

        float currentFrame = glfwGetTime();
        float deltaTime = currentFrame - lastFrame;
        lastFrame = currentFrame;

        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        processKeyboardInput(WINDOW, deltaTime);

        updateShaderProgram(SHADER_PROGRAM);

        render(DATA_COUNT);

        glfwSwapBuffers(WINDOW);
        glfwPollEvents();

        // if (deltaTime < TARGET_FRAME_TIME)
        //     glfwWaitEventsTimeout(TARGET_FRAME_TIME - deltaTime);
    }
}

EXPORT void close()
{
    glfwSetWindowShouldClose(WINDOW, true);
    glfwTerminate();
}

EXPORT void cleanUp()
{
    glDeleteVertexArrays(1, &_VAO);
    glDeleteBuffers(1, &_VBO);
    glDeleteBuffers(1, &_positionSSBO);
    glDeleteBuffers(1, &_scaleSSBO);
    glDeleteBuffers(1, &_colorSSBO);
    glDeleteBuffers(1, &_quatSSBO);
    glDeleteBuffers(1, &_alphaSSBO);
    glDeleteProgram(SHADER_PROGRAM);

    for (size_t i = 0; i < DATA_COUNT; i++)
        if (DATA[i].sh != NULL)
            free(DATA[i].sh);

    free(DATA);
}