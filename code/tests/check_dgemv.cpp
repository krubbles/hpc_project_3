#include <algorithm>
#include <cmath>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <cblas.h>

extern void my_dgemv(int, double*, double*, double*);

void require(bool condition, const std::string& message) {
    if (!condition) {
        throw std::runtime_error(message);
    }
}

void check_case(int n, std::vector<double> A, std::vector<double> x,
                std::vector<double> y, bool hand_computed = false) {
    const std::vector<double> initial_A = A;
    const std::vector<double> initial_x = x;
    std::vector<double> expected = y;
    // Two calls also catch implementations that overwrite rather than accumulate.
    for (int repetition = 0; repetition < 2; ++repetition) {
        if (n > 0) {
            cblas_dgemv(CblasRowMajor, CblasNoTrans, n, n,
                        1.0, initial_A.data(), n, initial_x.data(), 1, 1.0, expected.data(), 1);
        }
        my_dgemv(n, A.data(), x.data(), y.data());
        require(A == initial_A, "Kernel modified A");
        require(x == initial_x, "Kernel modified x");
        for (std::size_t i = 0; i < y.size(); ++i) {
            require(std::isfinite(y[i]) && std::isfinite(expected[i]), "Nonfinite result");
            const double tolerance = 1e-9 + 1e-11 * std::abs(expected[i]);
            require(std::abs(y[i] - expected[i]) <= tolerance,
                    "CBLAS mismatch: n=" + std::to_string(n) + ", row=" + std::to_string(i));
        }
        if (hand_computed) {
            require(y[0] == 7.0 + (repetition + 1) &&
                    y[1] == 11.0 + 7.0 * (repetition + 1),
                    "Hand-computed nonzero-y, row-major case failed");
        }
    }
}

int main() {
    try {
        check_case(0, {}, {}, {9.0});
        check_case(2, {1, 2, 3, 4}, {5, -2}, {7, 11}, true);
        for (int n : {1, 2, 3, 7, 31, 65}) {
            std::vector<double> A(static_cast<std::size_t>(n) * n);
            std::vector<double> x(n), y(n);
            for (int i = 0; i < n; ++i) {
                x[i] = ((i * 7) % 19 - 9) * (i % 2 ? 0.001 : 1000.0);
                y[i] = 0.5 + i / 3.0;
                for (int j = 0; j < n; ++j) {
                    // Asymmetric matrix with mixed signs; catches transposed indexing.
                    A[static_cast<std::size_t>(i) * n + j] = ((i * 13 + j * 5) % 23 - 11) / 7.0;
                }
            }
            check_case(n, A, x, y);
            std::fill(A.begin(), A.end(), 0.0);
            check_case(n, A, x, y);
            for (int i = 0; i < n; ++i) {
                A[static_cast<std::size_t>(i) * n + i] = 1.0;
            }
            check_case(n, A, x, y);
        }
        std::cout << "PASS: hand-computed case, CBLAS comparisons, accumulation, and unchanged inputs\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
