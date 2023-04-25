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
    // int s_ = atoi(argv[1]);
    // int t_ = atoi(argv[2]);
    
    // if (t_ < 4) {
    //     return 0;
    // }

    // const OUTER_BLOCK = s_;
    // const INNER_BLOCK = t_;

    // printf("\nt: %d, s: %d \n", t, s);

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
    
    // __m256d sum;
    // _VCRT_RESTRICT

    // Computation
    start = time(NULL);

    // #pragma loop(hint_parallel(0))
    #pragma loop(ivdep)
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            // #pragma loop(no_vector)
            for (int j = 0; j < n; j++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    // multiply(A, B, C);


    // #pragma loop(hint_parallel(0))
    // #pragma loop(ivdep)
    // for (int i = 0; i < n; i += OUTER_BLOCK) {
    //     for (int j = 0; j < n; j += OUTER_BLOCK) {
    //         for (int k = 0; k < n; k += OUTER_BLOCK) {
    //             for (int ii = 0; ii < OUTER_BLOCK; ii += INNER_BLOCK) {
    //                 for (int jj = 0; jj < OUTER_BLOCK; jj += INNER_BLOCK) {
    //                     for (int kk = 0; kk < OUTER_BLOCK; kk += INNER_BLOCK) {
    //                         for (int iii = 0; iii < INNER_BLOCK; iii++) {
    //                             for (int kkk = 0; kkk < INNER_BLOCK; kkk++) {
    //                                 for (int jjj = 0; jjj < INNER_BLOCK; jjj++) {
    //                                     C[i+ii+iii][j+jj+jjj] += A[i+ii+iii][k+kk+kkk] * B[k+kk+kkk][j+jj+jjj];
    //                                 }
    //                             }
    //                         }
    //                     }
    //                 }
    //             }
    //         }
    //     }
    // }

    end = time(NULL);

    double seconds = difftime(end, start);
    printf("%.f seconds\n", seconds); // 22 seconds
    return 0;
}




// void multiply(int A[][], int B[][], _VCRT_RESTRICT int C[][]) {
    
//     #pragma loop(hint_parallel(0))
//     #pragma loop(ivdep)
//     for (int i = 0; i < n; i += s) {
//         for (int j = 0; j < n; j += s) {
//             for (int k = 0; k < n; k += s) {
//                 for (int ii = 0; ii < s; ii += t) {
//                     for (int jm = 0; jm < s; jm += t) {
//                         for (int km = 0; km < s; km += t) {
//                             for (int iii = 0; iii < t; iii++) {
//                                 for (int jl = 0; jl < t; jl++) {
//                                     for (int kkk = 0; kkk < t; kkk++) {
//                                         C[i+ii+iii][j+jm+jl] += A[i+ii+iii][k+km+kkk] * B[k+km+kkk][j+jm+jl];
//                                     }
//                                 }
//                             }
//                         }
//                     }
//                 }
//             }
//         }
//     }
// }