cmake_minimum_required(VERSION 3.10)
project(RenderingLib)

set(CMAKE_C_STANDARD 11)

set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_C_COMPILER x86_64-w64-mingw32-gcc)
set(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++)

include_directories(
    lib/glfw-3.4/include
    lib/glew-2.1.0/include
    lib/cglm/include
    /usr/x86_64-w64-mingw32/include
)

link_directories(
    lib/glfw-3.4/lib-mingw-w64
    lib/glew-2.1.0/bin/Release/x64
    lib/cglm/build
    /usr/x86_64-w64-mingw32/lib
)

add_library(rendering_lib SHARED
    src/camera.c
    src/data.c
    src/loader.c
    src/main.c
    src/rendering.c
    src/shader.c
    src/main.c
)

target_link_libraries(rendering_lib
    cglm
    glfw3dll
    glew32
    opengl32
    gdi32
)

# set_target_properties(rendering_lib PROPERTIES
#     OUTPUT_NAME "rendering_lib"
#     PREFIX ""
#     SUFFIX ".dll"
# )
