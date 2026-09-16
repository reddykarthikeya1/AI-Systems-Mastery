// Standalone Production CUDA C++ Tiled GEMM Kernel
#include <iostream>
#include <vector>
#include <cmath>
#include <cuda_runtime.h>

#define TILE_SIZE 32

__global__ void tiled_gemm_kernel(const float *__restrict__ A,
                                  const float *__restrict__ B,
                                  float *__restrict__ C,
                                  int M, int N, int K) {
    __shared__ float sA[TILE_SIZE][TILE_SIZE];
    __shared__ float sB[TILE_SIZE][TILE_SIZE];

    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;
    float accum = 0.0f;

    int num_tiles = (K + TILE_SIZE - 1) / TILE_SIZE;
    for (int t = 0; t < num_tiles; ++t) {
        // Load into shared memory with bounds check
        int a_col = t * TILE_SIZE + threadIdx.x;
        int b_row = t * TILE_SIZE + threadIdx.y;

        sA[threadIdx.y][threadIdx.x] = (row < M && a_col < K) ? A[row * K + a_col] : 0.0f;
        sB[threadIdx.y][threadIdx.x] = (b_row < K && col < N) ? B[b_row * N + col] : 0.0f;
        __syncthreads();

        #pragma unroll
        for (int k = 0; k < TILE_SIZE; ++k) {
            accum += sA[threadIdx.y][k] * sB[k][threadIdx.x];
        }
        __syncthreads();
    }

    if (row < M && col < N) {
        C[row * N + col] = accum;
    }
}

int main() {
    const int M = 512, N = 512, K = 512;
    std::cout << "CUDA Tiled GEMM [512x512x512] compiled." << std::endl;
    return 0;
}
