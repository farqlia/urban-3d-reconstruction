#include "utils.h"

void getDegreeOrderHarmonic(int* L, int* M, size_t sh_count)
{
    *L = 0;
    *M = 0;

    int iter = 1;
    for (int i = -1; sh_count > 0; i+=2) {
        sh_count -= iter;
        (*L)++;
        (*M)++;
    }
}

// Sigmoid normalization function
float sigmoid(float x) {
    return 1.0f / (1.0f + expf(-x));
}

// Normalize a value to 0-255
unsigned char normalizeToColor(float value) {
    return (unsigned char)(sigmoid(value) * 255.0f);
}