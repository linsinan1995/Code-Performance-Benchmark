#include "linux-perf-events.h"
#include <cassert>
#include <cinttypes>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <libgen.h>
#include <random>
#include <string>
#include <vector>
#include <cmath>
#include <chrono>

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

#ifdef None
__attribute__((optimize("O2", "loop-interchange")))
void manual()
{
    int i,j,k;
    for (i = 0; i < N; i++){
        for (j = 0; j < M; j++){
            for (k = 0; k< P; k++){
                C[i][j] = C[i][j] + A[i][k] * B[k][j];
            }
        }       
    }
}
#endif 
#ifdef NPM
void manual()
{
    int i,j,k;
    for (i = 0; i < N; i++){
        for (k = 0; k< P; k++){
            for (j = 0; j < M; j++) {
                C[i][j] = C[i][j] + A[i][k] * B[k][j];
            }
        }       
    }
}
#endif

#ifdef NMP
void manual()
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
#endif

#ifdef PNM
void manual()
{
    int i,j,k;
    for (k = 0; k< P; k++){
        for (i = 0; i < N; i++){
	    for (j = 0; j < M; j++) {
		C[i][j] = C[i][j] + A[i][k] * B[k][j];
	    }
	}       
    }
}
#endif


#ifdef PMN
void manual()
{
    int i,j,k;
    for (k = 0; k< P; k++){
	for (j = 0; j < M; j++) {
        	for (i = 0; i < N; i++){
		C[i][j] = C[i][j] + A[i][k] * B[k][j];
	    }
	}       
    }
}
#endif


#ifdef MPN
void manual()
{
    int i,j,k;
    for (j = 0; j < M; j++) {
    	for (k = 0; k< P; k++){
            for (i = 0; i < N; i++){
		C[i][j] = C[i][j] + A[i][k] * B[k][j];
	    }
	}       
    }
}
#endif


#ifdef MNP
void manual()
{
    int i,j,k;
    for (j = 0; j < M; j++) {
        for (i = 0; i < N; i++){
    	    for (k = 0; k< P; k++){
		C[i][j] = C[i][j] + A[i][k] * B[k][j];
	    }
	}       
    }
}
#endif

typedef void (*bm)();

void test(bm fn) {

  initialize();
  size_t iterations = 5;
  std::vector<int> evts;
  evts.push_back(PERF_COUNT_HW_CPU_CYCLES);
  evts.push_back(PERF_COUNT_HW_INSTRUCTIONS);
  evts.push_back(PERF_COUNT_HW_BRANCH_MISSES);
  evts.push_back(PERF_COUNT_HW_CACHE_REFERENCES);
  evts.push_back(PERF_COUNT_HW_CACHE_MISSES);
  evts.push_back(PERF_COUNT_HW_REF_CPU_CYCLES);
  LinuxEvents<PERF_TYPE_HARDWARE> unified(evts);
  std::vector<unsigned long long> results;
  std::vector<std::vector<unsigned long long>> allresults;
  results.resize(evts.size());

  
  auto start = std::chrono::high_resolution_clock::now();
  for (uint32_t i = 0; i < iterations; i++) {
    unified.start();
    fn();
    unified.end(results);
    allresults.push_back(results);
  }
  auto end = std::chrono::high_resolution_clock::now();
  float temps_execution = std::chrono::duration<float, std::nano>(end-start).count();
  std::vector<unsigned long long> mins = compute_mins(allresults);
  std::vector<double> avg = compute_averages(allresults);
  std::vector<unsigned long long> maxs = compute_maxs(allresults);
  printf("average time:%2fms\n", temps_execution/(iterations*1000000.0));
  printf(
      "instructions per cycle %4.2f, cycles per pair of 32-bit words:  %4.3f, "
      "instructions per pair of 32-bit words: %4.3f \n",
      double(mins[1]) / mins[0], double(mins[0]) / N, double(mins[1]) / N);
  // first we display mins
  printf("min: %8llu cycles, %8llu instructions, \t%8llu branch mis., %8llu "
         "cache ref., %8llu cache mis.\n",
         mins[0], mins[1], mins[2], mins[3], mins[4]);
  printf("avg: %8.1f cycles, %8.1f instructions, \t%8.1f branch mis., %8.1f "
         "cache ref., %8.1f cache mis.\n",
         avg[0], avg[1], avg[2], avg[3], avg[4]);
  printf("max: %8llu cycles, %8llu instructions, \t%8llu branch mis., %8llu "
         "cache ref., %8llu cache mis.\n",
         maxs[0], maxs[1], maxs[2], maxs[3], maxs[4]);
  for (auto result : allresults)
  {
	  for (auto res : result)
	  	printf("%llu ", res);
	  printf("\n");
  }
}


int main() {  
  test(&manual);
}

// g++-8 -std=c++11 test.cpp -O2 -fno-dce -o test
