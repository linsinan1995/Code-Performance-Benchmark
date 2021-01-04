#include <chrono>
#include <cstdio> 
#include <cstdlib> 
#include <random>
#include <fstream>
using namespace std;

#define N 1500
#define M 1500
#define P 1500

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


void init_from_txt(const std::string& fileA, const std::string& fileB) {
    ifstream file_A(fileA);
    ifstream file_B(fileB);

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
        exit(1);
    }


#ifdef CHECK_ACCURACY
    init_from_txt("A.txt", "B.txt");
#else
    initialize();
#endif
    auto start = chrono::high_resolution_clock::now();
// benchmarking starts
    int i,j,k;
    for (i = 0; i < N; i++){
        for (j = 0; j < M; j++){
			for (k = 0; k + 7 - 1 < P; k+=7) {
            	C[i][j] = C[i][j] + A[i][k] * B[k][j];
            	C[i][j] = C[i][j] + A[i][k+1] * B[k+1][j];
            	C[i][j] = C[i][j] + A[i][k+2] * B[k+2][j];
            	C[i][j] = C[i][j] + A[i][k+3] * B[k+3][j];
            	C[i][j] = C[i][j] + A[i][k+4] * B[k+4][j];
            	C[i][j] = C[i][j] + A[i][k+5] * B[k+5][j];
            	C[i][j] = C[i][j] + A[i][k+6] * B[k+6][j];
			}
            for (; k < P; k++){
                C[i][j] = C[i][j] + A[i][k] * B[k][j];
            }
        }       
    }
// benchmarking ends
    auto end = chrono::high_resolution_clock::now();
    float temps_execution = chrono::duration<float, nano>(end-start).count();
    
    
#ifdef CHECK_ACCURACY
    for (int ii = 0; ii < N; ii++) {
        for (int jj = 0; jj < M; jj++) 
            printf("%.5f ", C[ii][jj]);
        printf("\n");
    } 
#else
    printf("%2f\n", C[row][col]);
    printf("Timer: \n%2f\n", temps_execution/1000.0);
#endif
    return 0;
}

// g++-10 -std=c++11 nounroll.cpp -O2 -fno-dce -floop-interchange -o test -fopt-info 
// -fopt-info-missed
