<!--
 * @Author: Lin Sinan
 * @Github: https://github.com/linsinan1995
 * @Email: mynameisxiaou@gmail.com
 * @LastEditors  : Lin Sinan
 * @Description: 
*               
*               
* https://gcc.gnu.org/onlinedocs/gcc-4.5.2/gcc/Optimize-Options.html          
 -->

# Environment

`version:gcc version 8.3.0 (Homebrew GCC 8.3.0_2)`


# Optimization in GCC

```
Without any optimization option, the compiler's goal is to reduce the cost of compilation and to make debugging produce the expected results. Statements are independent: if you stop the program with a breakpoint between statements, you can then assign a new value to any variable or change the program counter to any other statement in the function and get exactly the results you would expect from the source code.

Turning on optimization flags makes the compiler attempt to improve the performance and/or code size at the expense of compilation time and possibly the ability to debug the program.
```


Which set of optimizations will be invoked depends on the target and how GCC was configured.

we can use `gcc-8 -Q --help=optimizers` to check which optimizers are enabled in your machine.

# Optimization in different level

## default Optimization

`-O0`, Reduce compilation time and make debugging produce the expected results. This is the default.

## O1 level Optimization

In O1 level, using -O(-O1) turns on the following optimization flags:
```
        -fauto-inc-dec 
        -fcprop-registers 
        -fdce 
        -fdefer-pop 
        -fdelayed-branch 
        -fdse 
        -fguess-branch-probability 
        -fif-conversion2 
        -fif-conversion 
        -fipa-pure-const 
        -fipa-reference 
        -fmerge-constants
        -fsplit-wide-types 
        -ftree-builtin-call-dce 
        -ftree-ccp 
        -ftree-ch 
        -ftree-copyrename 
        -ftree-dce 
        -ftree-dominator-opts 
        -ftree-dse 
        -ftree-forwprop 
        -ftree-fre 
        -ftree-phiprop 
        -ftree-sra 
        -ftree-pta 
        -ftree-ter 
        -funit-at-a-time
```

-O also turns on `-fomit-frame-pointer` on machines where doing so does not interfere with debugging.


## O2 level Optimization

-O2 turns on all optimization flags specified by `-O`. It also turns on the following optimization flags:

```
        -fthread-jumps 
        -falign-functions  -falign-jumps 
        -falign-loops  -falign-labels 
        -fcaller-saves 
        -fcrossjumping 
        -fcse-follow-jumps  -fcse-skip-blocks 
        -fdelete-null-pointer-checks 
        -fexpensive-optimizations 
        -fgcse  -fgcse-lm  
        -finline-small-functions 
        -findirect-inlining 
        -fipa-sra 
        -foptimize-sibling-calls 
        -fpeephole2 
        -fregmove 
        -freorder-blocks  -freorder-functions 
        -frerun-cse-after-loop  
        -fsched-interblock  -fsched-spec 
        -fschedule-insns  -fschedule-insns2 
        -fstrict-aliasing -fstrict-overflow 
        -ftree-switch-conversion 
        -ftree-pre 
        -ftree-vrp
```

The warning under `-fgcse` about invoking `-O2` on programs that use computed gotos.

## O3 level Optimization

-O3 turns on all optimizations specified by -O2 and also turns on the `-finline-functions`, `-funswitch-loops`, `-fpredictive-commoning`, `-fgcse-after-reload`, `-ftree-vectorize` and `-fipa-cp-clone` options.

## Os level Optimization

Optimize for size. -Os enables all -O2 optimizations that do not typically increase code size. It also performs further optimizations designed to reduce code size.
-Os disables the following optimization flags:

```
          -falign-functions  -falign-jumps  -falign-loops 
          -falign-labels  -freorder-blocks  -freorder-blocks-and-partition 
          -fprefetch-loop-arrays  -ftree-vect-loop-version
```

# Specific Optimizers

["-O2", "-O2 -funroll-loops", "-O1", "-O0"],
## -ftree-dce

Removing dead code.

## -funroll-loops

Unroll loops whose number of iterations can be determined at compile time or upon entry to the loop. `-funroll-loops` implies `-frerun-cse-after-loop`. This option makes code larger, and may or may not make it run faster.

`-funroll-all-loops` is similar to `-funroll-loops`, but it also unrolles loops whose numbers of iterations are unknown at compile time, and `-funroll-all-loops` usually makes programs run more slowly.

# -floop-interchange



## -finline-functions

Integrate all simple functions into their callers. The compiler heuristically decides which functions are simple enough to be worth integrating in this way.

```
    -findirect-inlining
    -finline-small-functions
    -fno-inline
    -fearly-inlining
    -finline-limit=n
    -fkeep-inline-functions

    --param name=value
        max-inline-insns-auto
        max-inline-insns-single
```