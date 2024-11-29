#ifndef LOADER_H
#define LOADER_H

#include "stdlib.h"
#include "stdio.h"
#include "data.h"

int loadPLY(const char* filename, PointCloudData** data, size_t* pointCount);

#endif