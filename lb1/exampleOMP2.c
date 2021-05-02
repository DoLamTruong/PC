#include <omp.h>
#include<stdio.h>
/* Define some values */
#define N 1000
#define CHUNKSIZE 100
#define OMP_NUM_THREADS 10
#define MAX_THREADS 48
/* Global variables */
int main(int argc, char **argv){
int i, chunk;
float a[N], b[N], c[N];
/* Some initializations */
for(i = 0; i < N; i++){
a[i] = b[i] = i * 1.0; // values = i with float type
}
chunk = CHUNKSIZE;
#pragma omp parallel shared(a,b,c,chunk) private(i)
{
omp_set_num_threads(OMP_NUM_THREADS);
#pragma omp for schedule(dynamic,chunk) nowait
for(i = 0; i < N; i++){
int tid = omp_get_thread_num();
printf("Iter %d running from thread %d\n", i, tid);
c[i] = a[i] + b[i];
 }
}
/* Validation */
printf("Vector c: \n");
for(i = 0; i < 10; i++){
printf("%f ", c[i]);
}
printf("...\n");
/*
//
Statistic */
printf("Num of iter with thread:\n");
// for(i = 0; i < MAX_THREADS; i++){
// if(count[i] != 0)
// printf("\tThread %d run %d iter.\n", i, count[i]);
// }
return 0;
}