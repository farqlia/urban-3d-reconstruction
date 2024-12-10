#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#ifdef _WIN32
    #include <windows.h>
    #define LIBRARY_NAME "librendering_lib.dll"
#else
    #include <dlfcn.h>
    #define LIBRARY_NAME "rendering_lib.so"
#endif

int main() {
    // Shared library handle
    #ifdef _WIN32
    HMODULE lib_handle = (HMODULE)LoadLibrary(LIBRARY_NAME); // Explicit cast to HMODULE
    if (!lib_handle) {
        printf("Failed to load library: %s\n", LIBRARY_NAME);
        return -1;
    }
    #else
    void* lib_handle = dlopen(LIBRARY_NAME, RTLD_LAZY);
    if (!lib_handle) {
        printf("Failed to load library: %s\nError: %s\n", LIBRARY_NAME, dlerror());
        return -1;
    }
    #endif

    // Define function pointers
    void (*initWindow)();
    void (*loadData)(const char*);
    intptr_t (*getWindowId)();
    void (*run)();
    void (*close)();
    void (*cleanUp)();

    // Load functions from library
    #ifdef _WIN32
    initWindow = (void (*)())GetProcAddress(lib_handle, "initWindow");
    loadData = (void (*)(const char*))GetProcAddress(lib_handle, "loadData");
    getWindowId = (intptr_t (*)())GetProcAddress(lib_handle, "getWindowId");
    run = (void (*)())GetProcAddress(lib_handle, "run");
    close = (void (*)())GetProcAddress(lib_handle, "close");
    cleanUp = (void (*)())GetProcAddress(lib_handle, "cleanUp");
    #else
    initWindow = (void (*)())dlsym(lib_handle, "initWindow");
    loadData = (void (*)(const char*))dlsym(lib_handle, "loadData");
    getWindowId = (intptr_t (*)())dlsym(lib_handle, "getWindowId");
    run = (void (*)())dlsym(lib_handle, "run");
    close = (void (*)())dlsym(lib_handle, "close");
    cleanUp = (void (*)())dlsym(lib_handle, "cleanUp");
    #endif

    // Verify function pointers
    if (!initWindow || !loadData || !getWindowId || !run || !close || !cleanUp) {
        printf("Failed to load functions from library.\n");
        #ifdef _WIN32
        FreeLibrary(lib_handle);
        #else
        dlclose(lib_handle);
        #endif
        return -1;
    }

    // Initialize the window
    printf("Initializing window...\n");
    initWindow();

    // Load some data (provide a valid PLY file path)
    const char* ply_file = "example.ply";
    printf("Loading data from: %s\n", ply_file);
    loadData(ply_file);

    // Get the window ID
    intptr_t windowId = getWindowId();
    printf("Window ID: %ld\n", (long)windowId);

    // Run the rendering loop
    printf("Running rendering loop. Close the window to exit.\n");
    run();

    // Clean up resources
    printf("Cleaning up resources...\n");
    cleanUp();

    // Close library
    #ifdef _WIN32
    FreeLibrary(lib_handle);
    #else
    dlclose(lib_handle);
    #endif

    printf("Test complete.\n");
    return 0;
}
