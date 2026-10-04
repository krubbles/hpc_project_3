// (C) 2021, E. Wes Bethel. Reference implementation additions, 2026.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstddef>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
#include <cblas.h>

extern void my_dgemv(int, double*, double*, double*);
extern const char* dgemv_desc;

void reference_dgemv(int n, double* A, double* x, double* y) {
    cblas_dgemv(CblasRowMajor, CblasNoTrans, n, n,
                1.0, A, n, x, 1, 1.0, y, 1);
}

void fill(double* data, std::size_t count, std::mt19937& generator) {
    std::uniform_real_distribution<double> distribution(-1.0, 1.0);
    for (std::size_t i = 0; i < count; ++i) {
        data[i] = distribution(generator);
    }
}

bool check_accuracy(const double* expected, const double* actual, int n) {
    for (int i = 0; i < n; ++i) {
        // Optimized reductions may reorder additions, so allow rounding error.
        const double tolerance = 1e-10 + 1e-10 * std::abs(expected[i]);
        if (!std::isfinite(expected[i]) || !std::isfinite(actual[i]) ||
            std::abs(expected[i] - actual[i]) > tolerance) {
            std::cerr << "Verification failed at row " << i
                      << ": expected " << std::setprecision(17) << expected[i]
                      << ", got " << actual[i] << '\n';
            return false;
        }
    }
    return true;
}

std::vector<int> parse_sizes(int argc, char** argv) {
    if (argc == 1) {
        return {1024, 2048, 4096, 8192, 16384};
    }
    if (argc != 3 || std::string(argv[1]) != "--sizes") {
        throw std::invalid_argument("Usage: benchmark-* [--sizes N1,N2,...]");
    }
    const std::string input(argv[2]);
    std::vector<int> sizes;
    std::size_t start = 0;
    while (start < input.size()) {
        const std::size_t end = input.find(',', start);
        const std::string token = input.substr(start, end - start);
        if (token.empty() || token.find_first_not_of("0123456789") != std::string::npos) {
            throw std::invalid_argument("Sizes must be comma-separated positive integers");
        }
        const unsigned long long value = std::stoull(token);
        if (value == 0 || value > static_cast<unsigned long long>(std::numeric_limits<int>::max())) {
            throw std::invalid_argument("Problem size is outside the supported integer range");
        }
        sizes.push_back(static_cast<int>(value));
        if (end == std::string::npos) {
            break;
        }
        start = end + 1;
        if (start == input.size()) {
            throw std::invalid_argument("Size list must not end with a comma");
        }
    }
    if (sizes.empty()) {
        throw std::invalid_argument("At least one problem size is required");
    }
    return sizes;
}

int main(int argc, char** argv) {
    if (argc == 2 && std::string(argv[1]) == "--help") {
        std::cout << "Usage: benchmark-* [--sizes N1,N2,...]\n"
                     "Defaults: 1024,2048,4096,8192,16384; first size has a warmup run.\n";
        return 0;
    }
    try {
        std::vector<int> sizes = parse_sizes(argc, argv);
        // Keep the starter's extra first run to warm up BLAS; mark it explicitly.
        sizes.insert(sizes.begin(), sizes.front());
        const std::size_t max_size = *std::max_element(sizes.begin(), sizes.end());
        const std::size_t max_elements = std::vector<double>().max_size();
        if (max_size > max_elements / 4 ||
            max_size > (max_elements - 4 * max_size) / max_size / 2) {
            throw std::length_error("Problem size exceeds the supported allocation range");
        }
        const std::size_t matrix_elements = max_size * max_size;
        std::vector<double> buffer(2 * matrix_elements + 4 * max_size);
        double* A = buffer.data();
        double* Acopy = A + matrix_elements;
        double* x = Acopy + matrix_elements;
        double* xcopy = x + max_size;
        double* y = xcopy + max_size;
        double* ycopy = y + max_size;
        std::mt19937 generator(746);
        bool all_verified = true;
        std::cout << "# " << dgemv_desc << '\n'
                  << "n,seconds,flops,mflops,verified,warmup\n";
        for (std::size_t run = 0; run < sizes.size(); ++run) {
            const int n = sizes[run];
            const std::size_t elements = static_cast<std::size_t>(n) * n;
            fill(A, elements, generator);
            fill(x, n, generator);
            fill(y, n, generator);
            std::copy_n(A, elements, Acopy);
            std::copy_n(x, n, xcopy);
            std::copy_n(y, n, ycopy);

            const auto start = std::chrono::steady_clock::now();
            my_dgemv(n, A, x, y);
            const auto end = std::chrono::steady_clock::now();
            const double seconds = std::chrono::duration<double>(end - start).count();

            reference_dgemv(n, Acopy, xcopy, ycopy);
            const bool verified = check_accuracy(ycopy, y, n);
            all_verified = all_verified && verified;
            // n multiplications and n additions per row, including adding to y.
            const std::size_t flops = 2 * elements;
            const double mflops = seconds > 0.0 ? flops / seconds / 1e6
                : std::numeric_limits<double>::quiet_NaN();
            std::cout << n << ',' << std::scientific << std::setprecision(9)
                      << seconds << ',' << flops << ',' << mflops << ','
                      << (verified ? "PASS" : "FAIL") << ','
                      << (run == 0 ? 1 : 0) << '\n';
        }
        return all_verified ? 0 : 1;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
