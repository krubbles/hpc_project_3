#include <cstddef>

const char* dgemv_desc = "OpenMP dgemv.";

/* Y := A * X + Y. A is n-by-n, row-major; x and y are n-element vectors.
 * A and x are unchanged. The input and output buffers must not overlap.
 */
void my_dgemv(int n, double* A, double* x, double* y) {
    // Each thread owns distinct output rows; sum is local to each row.
    #pragma omp parallel for default(none) shared(n, A, x, y) schedule(static)
    for (int i = 0; i < n; ++i) {
        const double* row = A + static_cast<std::size_t>(i) * n;
        double sum = 0.0;
        for (int j = 0; j < n; ++j) {
            sum += row[j] * x[j];
        }
        y[i] += sum;
    }
}
