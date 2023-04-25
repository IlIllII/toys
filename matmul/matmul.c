#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define n 4096
#define OUTER_BLOCK 32
#define INNER_BLOCK 8
int A[n][n];
int B[n][n];
int C[n][n];

int main(int argc, const char *argv[]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) {
                A[i][j] = 1;
            } else {
                A[i][j] = 0;
            }
            B[i][j] = (double)j;
            C[i][j] = 0;
        }
    }

    time_t start, end;

    start = time(NULL);

    #pragma loop(ivdep)
    for (int ii = 0; ii < n; ii += OUTER_BLOCK) {
        for (int kk = 0; kk < n; kk += OUTER_BLOCK) {
            for (int jj = 0; jj < n; jj += OUTER_BLOCK) {
                for (int i = ii; i < ii + OUTER_BLOCK; i++) {
                    for (int k = kk; k < kk + OUTER_BLOCK; k++) {
                        for (int j = jj; j < jj + OUTER_BLOCK; j++) {
                            C[i][j] += A[i][k] * B[k][j];
                        }
                    }
                }
            }
        }
    }

    end = time(NULL);

    double seconds = difftime(end, start);
    printf("%.f seconds\n", seconds); 
    return 0;
}