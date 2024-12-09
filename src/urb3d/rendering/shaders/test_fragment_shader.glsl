#version 330 core

// Input from vertex shader
in vec3 color;

// Output to the screen
out vec4 outColor;

void main()
{
    // Output the color received from the vertex shader
    outColor = vec4(color, 1.0);  // RGBA color
}