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
#include <string>
#include <fstream>

#define display(mat, nRow, nCol) for (int i = 0; i < nRow; i++) { \
                                    for (int j = 0; j < nCol; j++) \
                                        printf("%4f ", mat[i][j]); \
                                printf("\n");} \
                                printf("\n")

#define getFloat() rand()/(float)(RAND_MAX/1.0);
#define _MIN(a,b) ((a) < (b) ? (a) : (b))
#define b 700  

using namespace std;

#define N 4000
#define M 3000
#define P 1000

float A[N][P];
float B[P][M];
float C[N][M];

string file_test;

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

void init_from_txt() {
    ifstream file_A("test/A.txt");
    ifstream file_B("test/B.txt");

    if (!file_A.is_open()) {
        printf("Doesn't find the file!\n") ;
    }

    
    for(int i=0;i<N;i++) {
        for(int j=0;j<P; j++) {
            file_A >> A[i][j];
        }
    }

    for(int i=0;i<P;i++) {
        for(int j=0;j<M; j++) {
            file_B >> B[i][j];
        }
    }

    // Close the File
    file_A.close();
    file_B.close();
}

void matrix_to_txt(const string & fileEnding) {
    ofstream file("test/C_" + fileEnding +  ".txt");

    if (!file.is_open()) {
        printf("Doesn't find the file!\n") ;
    }
    
    for(int i=0;i<N;i++) {
        for(int j=0;j<M; j++) {
            file  << C[i][j] << " ";
        }
        file << "\n";
    }

    // Close the File
    file.close();
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

#if TEST
    init_from_txt();
#else    
    srand((unsigned)time(NULL));
    initialize();
#endif
    auto start = chrono::high_resolution_clock::now();

 int i0, i, j0, j, k0, k;
 #if NMP
    for (i0 = 0; i0 < N; i0 += b)
        for (j0 = 0; j0 < M; j0 += b)
            for (k0 = 0; k0 < P; k0 += b)
                for (i = i0; i < _MIN(i0 + b, N); i++)
                    for (j = j0; j < _MIN(j0 + b, M); j++)
                        for (k = k0; k < _MIN(k0 + b, P); k++)         
#endif
 #if NPM
    for (i0 = 0; i0 < N; i0 += b)
        for (k0 = 0; k0 < P; k0 += b)
            for (j0 = 0; j0 < M; j0 += b)
                for (i = i0; i < _MIN(i0 + b, N); i++)
                    for (k = k0; k < _MIN(k0 + b, P); k++)         
                        for (j = j0; j < _MIN(j0 + b, M); j++)
#endif
 #if MNP
    for (j0 = 0; j0 < M; j0 += b)
        for (i0 = 0; i0 < N; i0 += b)
            for (k0 = 0; k0 < P; k0 += b)
                for (j = j0; j < _MIN(j0 + b, M); j++)
                    for (i = i0; i < _MIN(i0 + b, N); i++)
                        for (k = k0; k < _MIN(k0 + b, P); k++)         
#endif
 #if MPN
    for (j0 = 0; j0 < M; j0 += b)
        for (k0 = 0; k0 < P; k0 += b)
            for (i0 = 0; i0 < N; i0 += b)
                for (j = j0; j < _MIN(j0 + b, M); j++)
                    for (k = k0; k < _MIN(k0 + b, P); k++)     
                        for (i = i0; i < _MIN(i0 + b, N); i++)    
#endif
 #if PMN
    for (k0 = 0; k0 < P; k0 += b)
        for (j0 = 0; j0 < M; j0 += b)
            for (i0 = 0; i0 < N; i0 += b)
                for (k = k0; k < _MIN(k0 + b, P); k++)      
                    for (j = j0; j < _MIN(j0 + b, M); j++)
                        for (i = i0; i < _MIN(i0 + b, N); i++)   
#endif

 #if PNM
    for (k0 = 0; k0 < P; k0 += b)
        for (i0 = 0; i0 < N; i0 += b)
            for (j0 = 0; j0 < M; j0 += b)     
                for (k = k0; k < _MIN(k0 + b, P); k++) 
                    for (i = i0; i < _MIN(i0 + b, N); i++)   
                            for (j = j0; j < _MIN(j0 + b, M); j++)
#endif

 #if NORMAL
    for (i = 0; i < N; i++)
        for (j = 0; j < M; j++)
            for (k = 0; k< P; k++)
#endif

 #if BEST_INT
    for (i = 0; i < N; i++)
        for (k = 0; k< P; k++)
            for (j = 0; j < M; j++)
#endif
                            C[i][j] += A[i][k] * B[k][j];


    auto end = chrono::high_resolution_clock::now();
    float temps_execution = chrono::duration<float, nano>(end-start).count();

#if TEST
    matrix_to_txt(file_test);    
#endif 
    printf("%2f\n", C[row][col]);

    // display(C, N, M);
    // display(A, N, P);
    // display(B, P, M);
    printf("Timer: \n%2f\n", temps_execution/1000.0);
    
    return 0;
}