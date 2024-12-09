CC = gcc
CFLAGS = -std=c99 -fPIC
LIBS = -lGL -lGLEW -lglfw -lm -lX11
OUTPUT = rendering_lib.so

# Source files
SOURCES = main.c camera.c shader.c rendering.c loader.c data.c

all: $(OUTPUT)

# Build rule
$(OUTPUT): $(SOURCES)
	$(CC) -shared $(SOURCES) -o $(OUTPUT) $(CFLAGS) $(LIBS)

# Clean rule
clean:
	rm -f $(OUTPUT)
