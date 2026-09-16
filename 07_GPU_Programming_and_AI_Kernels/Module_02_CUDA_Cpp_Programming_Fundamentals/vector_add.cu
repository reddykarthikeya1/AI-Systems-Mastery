// Standalone Production CUDA C++ Vector Addition Kernel
#include <iostream>
#include <vector>
#include <cmath>
#include <cuda_runtime.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            std::cerr << "CUDA error at " << __FILE__ << ":" << __LINE__ << " code=" << err << " \"" << cudaGetErrorString(err) << "\" << std::endl; \
            exit(1); \
        } \
    } while (0)

__global__ void vector_add_kernel(const float *__restrict__ a,
                                  const float *__restrict__ b,
                                  float *__restrict__ c,
                                  int n) {
    int stride = gridDim.x * blockDim.x;
    for (int idx = blockIdx.x * blockDim.x + threadIdx.x; idx < n; idx += stride) {
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    const int N = 1 << 20; // 1M elements
    const size_t bytes = N * sizeof(float);

    std::vector<float> h_a(N, 1.0f);
    std::vector<float> h_b(N, 2.5f);
    std::vector<float> h_c(N, 0.0f);

    float *d_a, *d_b, *d_c;
    CUDA_CHECK(cudaMalloc(&d_a, bytes));
    CUDA_CHECK(cudaMalloc(&d_b, bytes));
    CUDA_CHECK(cudaMalloc(&d_c, bytes));

    CUDA_CHECK(cudaMemcpy(d_a, h_a.data(), bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_b, h_b.data(), bytes, cudaMemcpyHostToDevice));

    const int block_size = 256;
    const int grid_size = (N + block_size - 1) / block_size;
    vector_add_kernel<<<grid_size, block_size>>>(d_a, d_b, d_c, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_c.data(), d_c, bytes, cudaMemcpyDeviceToHost));

    // Verify
    bool correct = true;
    for (int i = 0; i < N; ++i) {
        if (std::fabs(h_c[i] - 3.5f) > 1e-5) {
            correct = false;
            break;
        }
    }
    std::cout << "CUDA Vector Add: " << (correct ? "PASSED" : "FAILED") << std::endl;

    CUDA_CHECK(cudaFree(d_a));
    CUDA_CHECK(cudaFree(d_b));
    CUDA_CHECK(cudaFree(d_c));
    return correct ? 0 : 1;
}
