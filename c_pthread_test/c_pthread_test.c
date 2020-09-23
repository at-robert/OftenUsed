#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include "child_thread.h"

int g_var = 0;

// 主程式
int main() {
  pthread_t t; // 宣告 pthread 變數
  pthread_create(&t, NULL, child, "Child"); // 建立子執行緒
  char cmd = '\0';
  int cnt = 0;

  child_test();
  // 主執行緒工作
  // for(int i = 0;i < 13;++i) {
  //   g_var++;
  //   printf("Master g_var = %d\n", g_var); // 每秒輸出文字
  //   sleep(1);
  // }

  while (1)
	{
		printf("--->please input a char \n");
		scanf("%c", &cmd);			
		if (cmd == ' ' || cmd == '\0' || cmd == 10)
			continue;
		cnt++;	
		printf("---->cmd : %x === cnt : %d\n", cmd, cnt);
		switch(cmd)
		{
			case '+':
			{
				// ret = ioctl(mZoomFd, AN41908A_ZOOM_IN, &zoom);		
        g_var = 9;		
        printf("Master g_var = %d\n", g_var);
				break;
			}
			case '-':
			{
				// ret = ioctl(mZoomFd, AN41908A_ZOOM_OUT, &zoom);	
        g_var = 8;		
        printf("Master g_var = %d\n", g_var);		
				break;
			}
			case 'q':
			{
				// AFzoomClose();
				exit(1);
				break;
			}

      case 't':
			case '\n':
			{
				// ret = ioctl(mZoomFd, AN41908A_ZOOM_IN, &zoom);
        g_var = 55;		
        printf("Master g_var = %d\n", g_var);
				break;
			}
			default:
			{
				// ret = ioctl(mZoomFd, AN41908A_ZOOM_STOP, &zoom);
				break;
			}
		}
  }

  pthread_join(t, NULL); // 等待子執行緒執行完成
  return 0;
}