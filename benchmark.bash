#!/usr/bin/env bash
set -e

LAB=lab0
CPU=i7-7700HQ
BUILD_DIR=./build
REPORT_DIR=./reports/$CPU

if [ $# -ge 0 -a "$1" == '--debug' ]; then
    # Debug benchmark size
    BENCHMARK_ITERATIONS=1
else
    # Original benchmark size
    BENCHMARK_ITERATIONS=10
fi

function clean {
    if [ -d "$BUILD_DIR" ]; then
        echo "removing $BUILD_DIR"
        rm --recursive "$BUILD_DIR"
    fi
}

function echo_red {
    echo -e "\e[31m$@\e[0m"
}

function echo_header {
    echo -e "\e[1m$@\e[0m"
}

# make dirs for puting report results and compiled codes
if [ "$LAB" == "lab0" ]; then
    mkdir --verbose --parents ${BUILD_DIR}/$LAB
    mkdir --verbose --parents ${REPORT_DIR}/$LAB/{warm-up,tired-compilation}
fi

if [ "$LAB" == "lab1" ]; then
    mkdir --verbose --parents ${REPORT_DIR}/$LAB/{gcc,clang,icc,java}
fi


echo_red "======Start Building======"
if [ "$LAB" == "lab0" ]; then
    python3 build.py --build
fi

echo_red "======Start Testing======="

if [ "$LAB" == "lab0" ]; then
    python3 build.py
fi
