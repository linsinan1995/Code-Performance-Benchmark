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

#if UNROLL_TYPE == 1
__attribute__((optimize("O2"))) inline void
unroll() {
    int i,j,k;
    for (i = 0; i < N; i++){
        for (j = 0; j < M; j++){
            for (k = 0; k + 7 - 1 < P; k+=7)
	    {
		C[i][j] = C[i][j] + A[i][k] * B[k][j];
                C[i][j] = C[i][j] + A[i][k+1] * B[k+1][j];
                C[i][j] = C[i][j] + A[i][k+2] * B[k+2][j];
                C[i][j] = C[i][j] + A[i][k+3] * B[k+3][j];
                C[i][j] = C[i][j] + A[i][k+4] * B[k+4][j];
                C[i][j] = C[i][j] + A[i][k+5] * B[k+5][j];
                C[i][j] = C[i][j] + A[i][k+6] * B[k+6][j];
	    }
	    for (; k < P; k++)
		C[i][j] = C[i][j] + A[i][k] * B[k][j];
        }
    }
}
#elif UNROLL_TYPE == 2
__attribute__((optimize("O2"))) inline void
unroll()
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

#elif UNROLL_TYPE == 3
__attribute__((optimize("O2", "unroll-loops"))) inline void
unroll() {
    int i,j,k;
    for (i = 0; i < N; i++){
        for (j = 0; j < M; j++){
#pragma GCC unroll 7
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

  std::vector<float> time_record {};

  for (uint32_t i = 0; i < iterations; i++) {
    // timer starts
    auto start = std::chrono::high_resolution_clock::now();
    // perf event counter reset
    unified.start();
    fn();
    unified.end(results);
    allresults.push_back(results);
    auto end = std::chrono::high_resolution_clock::now();
    float temps_execution = std::chrono::duration<float, std::nano>(end-start).count();
    time_record.push_back(temps_execution);
  }


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
  std::string type {};
  if (UNROLL_TYPE == 1) type = "manual unroll 7";
  else if (UNROLL_TYPE == 3) type = "unroll";
  else if (UNROLL_TYPE == 2) type = "no unroll";
  else throw "error";
  printf("unroll: %s\n", type.c_str());
  test(&unroll);
}

// g++-8 -std=c++11 test.cpp -O2 -fno-dce -o test
