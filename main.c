 /*
 * @Author: Lin Sinan
 * @Github: https://github.com/linsinan1995
 * @Email: mynameisxiaou@gmail.com
 * @LastEditors  : Lin Sinan
 * @Description: 
 * 
    sysctl -a | grep cache
    hw.l1icachesize: 32768 bytes
    hw.l1dcachesize: 32768 bytes
    hw.l2cachesize: 262144 bytes
    hw.l3cachesize: 3145728 bytes                       
 *               
 *               
 */

#include <sys/time.h>
#include "include/tool.h"

#define N 4000
#define M 5000
#define P 500


float A[N][P];
float B[P][M];
float C[N][M];

void initialize() {
    int i,j;
    for (i = 0; i < N; i++) {
        for (j = 0; j < P; j++) {
            A[i][j] = getFloat();
        }
    }

    for (i = 0; i < P; i++) {
        for (j = 0; j < M; j++) {
            B[i][j] = getFloat();
        }
    }
}

// void initialize(char* filepath) {
//     for (int i = 0; i < N; i++) {
//         for (int j = 0; j < M; j++) {
//             C[i][j] = getFloat();
//         }
//     }

//     for (int i = 0; i < N; i++) {
//         for (int j = 0; j < P; j++) {
//             A[i][j] = getFloat();
//         }
//     }
// }

int main(int argc, char *argv[])
{
    if (argc != 3) {
        printf("Require 2 parameters, but it gets %d.\n", argc-1);
        return 1;
    }
    
    int row = atoi(argv[1]);
    int col = atoi(argv[2]);

    if (row >= N || col >= M) {
        printf("Index is out of the matrix size\n");
        return 2;
    }
    
    srand((unsigned)time(NULL));
    initialize();
    struct timeval start, end;


    gettimeofday(&start, NULL);
    int i,j,k;
    for (i = 0; i < N; i++){
        for (j = 0; j < M; j++){
           for (k = 0; k< P; k++){
               C[i][j] = C[i][j] + A[i][k] * B[k][j];
            }
        }       
    }
    gettimeofday(&end, NULL);

    
    float temps_execution= (float) ((end.tv_sec - start.tv_sec) *1000000 + end.tv_usec - start.tv_usec);
    printf("%2f\n", C[row][col]);
    printf("%2f\n", A[row][col]);
    
    // display(C, N, M);
    // display(A, N, P);
    // display(B, P, M);
    printf("Timer: \n%2f\n", temps_execution);
    
    return 0;
}