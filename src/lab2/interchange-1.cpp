/*
 * @Author: Lin Sinan
 * @Github: https://github.com/linsinan1995
 * @Email: mynameisxiaou@gmail.com
 * @LastEditors: Lin Sinan
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

#include <chrono>
#include <stdio.h> 
#include <stdlib.h> 

#define display(mat, nRow, nCol) for (int i = 0; i < nRow; i++) { \
                                    for (int j = 0; j < nCol; j++) \
                                        printf("%4f ", mat[i][j]); \
                                printf("\n");} \
                                printf("\n")

#define getFloat() rand()/(float)(RAND_MAX/1.0);


using namespace std;

#define N 2000
#define M 3000
#define P 200

float A[N][P];
float B[P][M];
float C[N][M];

inline void initialize() {
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


int main(int argc, char *argv[])
{
    if (argc != 3) {
        printf("Require 2 parameters, but it gets %d.\n", argc-1);
        exit(1);
    }
    
    int row = atoi(argv[1]);
    int col = atoi(argv[2]);

    if (row >= N || col >= M) {
        printf("Index is out of the matrix size\n");
        exit(2);
    }
    
    srand((unsigned)time(NULL));
    initialize();
    auto start = chrono::high_resolution_clock::now();
 
 
    int i,j,k;
    #pragma noparallel
    for (i = 0; i < M; i++){
        for (j = 0; j < N; j++){
           for (k = 0; k< P; k++){
               C[j][i] = C[j][i] + A[j][k] * B[k][i];
            }
        }       
    }

    auto end = chrono::high_resolution_clock::now();
    float temps_execution = chrono::duration<float, nano>(end-start).count();
    
    printf("%2f\n", C[row][col]);
    printf("%2f\n", A[row][col]);
    
    // display(C, N, M);
    // display(A, N, P);
    // display(B, P, M);
    printf("Timer: \n%2f\n", temps_execution/1000.0);
    
    return 0;
}