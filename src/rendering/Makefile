CC = gcc
CFLAGS = -Wall -g -std=c99
LIBS = -lGL -lGLEW -lglfw -lm

# Source files
SOURCES = main.c camera.c shader.c rendering.c loader.c data.c utils.c

# Output executable
OUTPUT = main

# Build rule
$(OUTPUT): $(SOURCES)
	$(CC) $(SOURCES) -o $(OUTPUT) $(CFLAGS) $(LIBS)

# Clean rule
clean:
	rm -f $(OUTPUT)
