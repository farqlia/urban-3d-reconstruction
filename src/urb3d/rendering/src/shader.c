#include "shader.h"

GLuint compileShader(GLenum shaderType, const char* shaderFilename)
{
    GLuint shader = glCreateShader(shaderType);
    char* shaderSource = loadShaderSource(shaderFilename);
    glShaderSource(shader, 1, &shaderSource, NULL);
    glCompileShader(shader);

    GLint success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success)
    {
        char infoLog[512];
        glGetShaderInfoLog(shader, 512, NULL, infoLog);
        printf("ERROR::SHADER::COMPILATION_FAILED\n%s\n", infoLog);
    }

    return shader;
}

GLuint createShaderProgram()
{
    GLuint vertexShader = compileShader(GL_VERTEX_SHADER, "src/urb3d/rendering/shaders/test_vertex_shader.glsl");
    GLuint fragmentShader = compileShader(GL_FRAGMENT_SHADER, "src/urb3d/rendering/shaders/test_fragment_shader.glsl");

    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    // Check for linking errors
    GLint success;
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
    if (!success)
    {
        char infoLog[512];
        glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
        printf("ERROR::PROGRAM::LINKING_FAILED\n%s\n", infoLog);
    }

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    return shaderProgram;
}

char* loadShaderSource(const char* filename) {
        FILE* file = fopen(filename, "r");  // Open file for reading
    if (!file) {
        fprintf(stderr, "Failed to open shader file: %s\n", filename);
        perror("Error details");  // Optionally add this for detailed error information
        return NULL;
    }

    // Move to the end of the file to find the size
    fseek(file, 0, SEEK_END);
    long fileSize = ftell(file);
    fseek(file, 0, SEEK_SET);

    // Allocate memory for the file contents + null terminator
    char* source = (char*)malloc(fileSize + 1);
    if (!source) {
        perror("Failed to allocate memory for shader source");
        fclose(file);
        return NULL;
    }

    // Read the file contents into the buffer
    fread(source, 1, fileSize, file);
    source[fileSize] = '\0';  // Null-terminate the string

    fclose(file);  // Close the file
    return source;  // Return the shader source
}

void setupShaderProgram(GLuint shaderProgram, mat4 model, mat4 projection)
{
    glUseProgram(shaderProgram);

    GLint projLoc = glGetUniformLocation(shaderProgram, "projection");
    GLint modelLoc = glGetUniformLocation(shaderProgram, "model");

    glUniformMatrix4fv(projLoc, 1, GL_FALSE, (const GLfloat*)projection);
    glUniformMatrix4fv(modelLoc, 1, GL_FALSE, (const GLfloat*)model);
}

void updateShaderProgram(GLuint shaderProgram)
{
    GLint viewLoc = glGetUniformLocation(shaderProgram, "view");
    GLint eyeLoc = glGetUniformLocation(shaderProgram, "eye");

    mat4 view;
    vec3 temp;
    glm_vec3_add(camera.position, camera.front, temp);
    glm_lookat(camera.position, temp, camera.up, view);

    glUniformMatrix4fv(viewLoc, 1, GL_FALSE, (const GLfloat*)view);
    glUniform3fv(eyeLoc, 1, camera.position);
}
