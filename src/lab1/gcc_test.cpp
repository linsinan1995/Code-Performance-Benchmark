#include <iostream>
#include <chrono>
#include <random>

#define N 2100
#define M 1600
#define P 2000

float A[N][P];
float B[P][M];
float C[N][M];



void initialize() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(1.0, 10.0);
    int i,j;
    for (i = 0; i < N; i++) {
        for (j = 0; j < P; j++) {
            A[i][j] = dis(gen);
        }
    }

    for (i = 0; i < P; i++) {
        for (j = 0; j < M; j++) {
            B[i][j] = dis(gen);
        }
    }
}

void interchange_manual()
{
    int i,j,k;
    for (i = 0; i < N; i++){
            for (j = 0; j < M; j++) {
                for (k = 0; k< P; k++){
                    C[i][j] = C[i][j] + A[i][k] * B[k][j];
            }
        }       
    }
}

int main()
{
    initialize();
    interchange_manual();
}
// g++-8 -std=c++11 gcc_test.cpp -O2 -fno-dce -floop-interchange -o test -fopt-info-loop
// -fopt-info-missed
// -fdump-ipa-all
// -fdump-tree-linterchange-details