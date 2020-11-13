/*
 *  Author:
 *      Indestinee
 *  Date:
 *      2016/10/20
 */

#include <bits/stdc++.h>
#include <sys/time.h>
using namespace std;
char buff[256], buff1[256], buff2[256], *p = buff;
int main(int argc, char **argv) {
    for (int i = 1; i < argc; i++) {
        sprintf(p, "%s ", argv[i]);
        while (*p)
            p++;
    }
    timeval a, b;
    gettimeofday(&a, NULL);
    int ret = system(buff);
    gettimeofday(&b, NULL);
    b.tv_sec -= a.tv_sec;
    b.tv_usec -= a.tv_usec;
    if (b.tv_usec < 0) {
        b.tv_usec += 1000000;
        b.tv_sec--;
    }
    puts("");
    puts("\033[1;34;m------------------------------------------------------------\033[0m");
    
    sprintf(buff1, "\033[1;%d;m%x %s\033[0m", ret?31:32, ret, ret?":(":":)");
    int sec = b.tv_sec;
    if (sec >= 3600) {
        sprintf(buff2, "\033[1;31;m%dh %dm\033[0m\n",
                sec/3600, sec%3600/60);
    } else if (sec >= 60) {
        sprintf(buff2, "\033[1;33;m%dm %ds\033[0m\n",
                sec/60, sec%60);
    } else if (sec) {
            sprintf(buff2, "\033[1;34;m%d.%03d s\033[0m\n",
                sec, int(b.tv_usec/1000));
    } else {
        sprintf(buff2, "\033[1;32;m%d.%03d ms\033[0m\n",
            int(b.tv_usec / 1000), int(b.tv_usec % 1000));
    }
    printf("Process returned %s    execution time %s", buff1, buff2);
    if (ret != 0)
        printf("\033[1;31;mRun Time Error!!! :(\033[0m\n");
    return 0;
}
