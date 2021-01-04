#include <chrono>
#include <cstdio> 
#include <cstdlib> 

using namespace std;

#define display(mat, nRow, nCol) for (int i = 0; i < nRow; i++) { \
                                    for (int j = 0; j < nCol; j++) \
                                        printf("%4f ", mat[i][j]); \
                                printf("\n");} \
                                printf("\n")


#define N 1500 
#define M 1500
#define P 1500

float A[N][P];
float B[P][M];
float C[N][M];

float getFloat() {
    return rand()/(float)(RAND_MAX/1.0);
}


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
    for (i = 0; i < N; i++){
        for (j = 0; j < M; j++){
            for (k = 0; k< P; k++) {
#pragma GCC unroll 7
                C[i][j] = C[i][j] + A[i][k] * B[k][j];
            }
        }       
    }

    auto end = chrono::high_resolution_clock::now();
    float temps_execution = chrono::duration<float, nano>(end-start).count();
    
    printf("%2f\n", C[row][col]);

    printf("Timer: \n%2f\n", temps_execution/1000.0);
    
    return 0;
}

// g++-10 -std=c++11 nounroll.cpp -O2 -fno-dce -floop-interchange -o test -fopt-info 
// -fopt-info-missed
