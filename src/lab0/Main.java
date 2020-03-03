/*
* @Author: Lin Sinan
* @Github: https://github.com/linsinan1995
* @Email: mynameisxiaou@gmail.com
 * @LastEditors: Lin Sinan
* @Description: 
*               
*               
*               
*/


public class Main {
    final static int N = 1000;
    final static int M = 200;
    final static int P = 500;

    final static float MIN = 0f;
    final static float MAX = 1f;

    float[][] A = new float[N][P];
    float[][] B = new float[P][M];
    float[][] C = new float[N][M];

    Main() {
        int i, j;
        for (i = 0; i < N; i++) {
            for (j = 0; j < P; j++) {
                A[i][j] = MIN + (float)Math.random() * (MAX - MIN);
            }
        }

        for (i = 0; i < P; i++) {
            for (j = 0; j < M; j++) {
                B[i][j] = MIN + (float)Math.random() * (MAX - MIN);
            }
        }
    }

    void computition() {
        int i,j,k;
        for (i = 0; i < N; i++){
            for (j = 0; j < M; j++){
                for (k = 0; k< P; k++){
                    C[i][j] = C[i][j] + A[i][k] * B[k][j];
                }
            }       
        }
    }

    static void display(float mat[][], int nRow, int nCol) {
        for (int i = 0; i < nRow; i++) { 
            for (int j = 0; j < nCol; j++) {
                System.out.printf("%4f ", mat[i][j]);
            }
            System.out.println();
        }
        System.out.println();
    }
    
    
    public static void main(String []args) {
        long startTime, stopTime;

        if (args.length != 2) {
            System.out.println("Please input row and col parameters");
            System.exit(1);
        }
        
        Main mat = new Main();
        for (int i = 0; i < 200; i++ ) {
            startTime = System.nanoTime();
            mat.computition();
            stopTime = System.nanoTime();
            long elapsedTime = stopTime - startTime;
            float time = (float)elapsedTime/1000f; // nanosec to microsec
            System.out.printf(" %4f\n",  time);
        }
        // display(mat.A, N, P);
        // display(mat.B, P, M);
        // display(mat.C, N, M);
    }
}
