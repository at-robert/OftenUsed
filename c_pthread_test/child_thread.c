#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include "child_thread.h"

extern int g_var;

// 子執行緒函數
void* child(void* data) {
  char *str = (char*) data; // 取得輸入資料
  int l_var = 0;
  // for(int i = 0;i < 13;++i) {
  //   printf("%s , g_var in child = %d\n", str, g_var); // 每秒輸出文字
  //   sleep(1);
  // }

  while(1){
    if(g_var != l_var){
      printf("%s , g_var in child = %d\n", str, g_var); //
      l_var = g_var;

      if(g_var == 55){
        break;
      }
    }

  }

  printf("child exit !!!! \n");
  pthread_exit(NULL); // 離開子執行緒
}

void child_test(void)
{
 printf("child_test!!! \n");
}