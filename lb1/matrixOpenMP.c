#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(){
  int n;
  printf("Type in a number \n");
	scanf("%d", &n);
  // This problem scales as n^3. 
  // This value may need to be adjusted

  double * A = (double*) malloc(sizeof(double)*n*n);
  double * B = (double*) malloc(sizeof(double)*n*n);
  double * C = (double*) malloc(sizeof(double)*n*n);
  
  printf("Carrying out matrix-matrix multiplication use OpenMP\n");

  // Cilk Plus array notation
  for (int i = 0 ; i < n; i++) {
    for(int j = 0; j < n; j++) {
      A[i*n+j]=(double)i/(double)n;
      B[i*n+j]=(double)j/(double)n;
    }
  }


  // C[0:n*n]=0.0;
  for (int i = 0; i < n*n; i++)
    C[i]=0.0;
  // C = A x B
  double time = omp_get_wtime();
  #pragma omp parallel default(none) shared(n, A, B, C)
  {
  
    #pragma omp for nowait collapse(3)                                                    

    for ( int i = 0 ; i < n ; i++){
      for ( int j = 0 ; j < n ; j++) {
        for ( int k = 0 ; k < n ; k++) {
          C[i*n+j] += A[i*n+k]*B[k*n+j];
        }
      }
    }
  }
  time = omp_get_wtime() - time;
  
  printf("Checking the results...\n");
  double norm = 0.0;
  for ( int i = 0 ; i < n ; i++)
    for ( int j = 0 ; j < n ; j++)
      norm += (C[i*n+j]-(double)(i*j)/(double)n)*(C[i*n+j]-(double)(i*j)/(double)n);
  
  if (norm > 1e-10)
    printf("Something is wrong... Norm is equal to %f\n", norm);
  else
    printf("Yup, we're good!\n");

  printf("Computing time: %f\n", time);  
  free(A);
  free(B);
  free(C);
}
