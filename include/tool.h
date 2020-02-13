/*
 * @Author: Lin Sinan
 * @Github: https://github.com/linsinan1995
 * @Email: mynameisxiaou@gmail.com
 * @LastEditors  : Lin Sinan
 * @Description: 
 *               
 *               
 *               
 */

#ifndef MYMATRIX_GENERATOR_H
#define MYMATRIX_GENERATOR_H

#include <stdio.h> 
#include <stdlib.h> 

#define display(mat, nRow, nCol) for (int i = 0; i < nRow; i++) { \
                                    for (int j = 0; j < nCol; j++) \
                                        printf("%4f ", mat[i][j]); \
                                printf("\n");} \
                                printf("\n")

#define getFloat() rand()/(float)(RAND_MAX/1.0);



#endif // MYMATRIX_GENERATOR_H