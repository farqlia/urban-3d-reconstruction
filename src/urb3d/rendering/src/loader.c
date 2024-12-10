#include "loader.h"

int loadPLY(const char* filename, PointCloudData** data, size_t* pointCount) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Error opening file: %s\n", filename);
        return -1;
    }

    char line[2048];
    int isFirstType = 0;
    size_t count = 0;
    size_t shCount = 0;

    // Check file type based on header content
    while (fgets(line, sizeof(line), file)) {
        if (strncmp(line, "element splat", 13) == 0) {
            sscanf(line, "element splat %d", &count);
        } else if (strncmp(line, "element vertex", 14) == 0) {
            sscanf(line, "element vertex %d", &count);
        } else if (strncmp(line, "property float sh", 17) == 0) {
            isFirstType = 1;
            shCount++;
        } else if (strncmp(line, "property uchar red", 18) == 0) {
            isFirstType = 0;
        }
         else if (strncmp(line, "end_header", 10) == 0) {
            break;
        }
    }

    shCount /= 3;

    *pointCount = count;

    // Allocate memory for data based on the number of points
    PointCloudData* points = malloc(*pointCount * sizeof(PointCloudData));
    for (size_t i = 0; i < *pointCount; i++) {
        points[i].sh_count = shCount;
        if (shCount != 0)
            points[i].sh = malloc(shCount * 3 * sizeof(float));
        else
            points[i].sh = NULL;
    }

    // Read each point's data
    size_t idx = 0;
    while (fgets(line, sizeof(line), file)) {
        if (line[0] == '\0') continue;  // Skip empty lines

        if (isFirstType) {
            // First type: Harmonic values
            sscanf(line, "%f %f %f %f %f %f %f %f %f %f %f",
                   &points[idx].position[0], &points[idx].position[1], &points[idx].position[2],
                   &points[idx].a, &points[idx].quaternition[0], &points[idx].quaternition[1],
                   &points[idx].quaternition[2], &points[idx].quaternition[3], &points[idx].scalars[0],
                   &points[idx].scalars[1], &points[idx].scalars[2]);
            
            for (size_t j = 0; j < shCount * 3; j++) {
                sscanf(line, "%f", &points[idx].sh[j]);
            }
            // Example: Allocate harmonic values dynamically if needed
        } else {
            // Second type: Color values
            int colors[3];
            sscanf(line, "%f %f %f %d %d %d %f %f %f %f %f %f %f %f",
                   &points[idx].position[0], &points[idx].position[1], &points[idx].position[2],
                   &colors[0], &colors[1], &colors[2],
                   &points[idx].a, &points[idx].quaternition[0], &points[idx].quaternition[1],
                   &points[idx].quaternition[2], &points[idx].quaternition[3], &points[idx].scalars[0],
                   &points[idx].scalars[1], &points[idx].scalars[2]);
            points[idx].color[0] = (float)colors[0];
            points[idx].color[1] = (float)colors[1];
            points[idx].color[2] = (float)colors[2];
        }
        idx++;
    }

    fclose(file);
    *data = points;
    return 0;
}