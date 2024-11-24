# Installation

## For windows 
https://medium.com/swlh/setting-opengl-for-windows-d0b45062caf

## Core utility

- ***libglfw3***, ***libglfw3-dev*** - GLFW libraries for managing OpenGL

- ***libglew-dev*** - helper to manage OpenGL extensions

- ***libgl1-mesa-dev*** - OpenGL libraries and headers

```
sudo apt install libglfw3 libglfw3-dev libglew-dev libgl1-mesa-dev
```

# Testing

## Test code

### Code

```c
#include <GLFW/glfw3.h>
#include <stdio.h>

int main(void) {
    // Initialize GLFW
    if (!glfwInit()) {
        fprintf(stderr, "Failed to initialize GLFW\n");
        return -1;
    }

    // Create a windowed mode window and its OpenGL context
    GLFWwindow* window = glfwCreateWindow(640, 480, "GLFW Test Window", NULL, NULL);
    if (!window) {
        fprintf(stderr, "Failed to create GLFW window\n");
        glfwTerminate();
        return -1;
    }

    // Make the window's OpenGL context current
    glfwMakeContextCurrent(window);

    // Set the swap interval (for vsync)
    glfwSwapInterval(1); // Enable vsync

    // Main loop: keep the window open until the user closes it
    while (!glfwWindowShouldClose(window)) {
        // Set the background color (RGB format)
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f); // Dark teal color
        glClear(GL_COLOR_BUFFER_BIT); // Clear the screen with the color

        // Swap front and back buffers
        glfwSwapBuffers(window);

        // Poll for and process input events
        glfwPollEvents();

        // Close window when the ESC key is pressed
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
            glfwSetWindowShouldClose(window, 1);
        }
    }

    // Clean up and close the GLFW window
    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}
```

### Compilation

```
gcc -o main main.c -lGL -lglfw
```

### Execution

```
./main
```
