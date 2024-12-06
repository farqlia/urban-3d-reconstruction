CC = gcc
CFLAGS = -std=c99 -fPIC

UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S), Linux)
	LIBS = -lGL -lGLEW -lglfw -lm -lX11
	OUTPUT = rendering_lib.so
else ifeq ($(UNAME_S), CYGWIN)
	LIBS = -lopengl32 -lGLEW -lglfw3 -lm -lX11
	OUTPUT = rendering_lib.dll
else ifeq ($(UNAME_S), MINGW32_NT)
	LIBS = -lopengl32 -lGLEW -lglfw3 -lm -lgdi32 -luser32
	OUTPUT = rendering_lib.dll
else
	$(error Unsupported OS: $(UNAME_S))
endif

# Source files
SOURCES = main.c camera.c shader.c rendering.c loader.c data.c utils.c

all: $(OUTPUT)

# Build rule
$(OUTPUT): $(SOURCES)
	$(CC) -shared $(SOURCES) -o $(OUTPUT) $(CFLAGS) $(LIBS)

# Clean rule
clean:
	rm -f $(OUTPUT)
