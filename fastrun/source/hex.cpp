/*
 *  Author:
 *      Indestinee
 *  Date:
 *      2016/11/30
 */
#include <bits/stdc++.h>
using namespace std;
const int base = 16, maxn = 1 << 10, mask = maxn - 1;
int option = 1;
char buff[maxn], out[2][maxn], *p0, *p1;
void hex(char *buff, const int &len, const int &add = 0) {
    p0 = out[0];
    for (int j = 0; j < base; j++) {
        //  00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F
        sprintf(p0, "%02X%s", j, j + 1 == base ? "" : j + 1 == (base >> 1) ? "  " : " ");
        while (*p0)
            p0++;
    }
    printf("Address:  %s  Data:\n", out[0]);

    //  extend to nlen
    int nlen = len + (base - len % base) % base;
    memset(buff + len, 0, nlen - len);

    for (int i = 0; i < nlen; i += base) {
        p0 = out[0], p1 = out[1];
        for (int j = 0; j < base; j++) {
            sprintf(p0, "%02x%s", buff[i | j] & 0xff, j + 1 == base ? "" : j + 1 == (base >> 1) ? "  " : " ");
            while (*p0)
                p0++;
            sprintf(p1++, "%c", (buff[i | j] > 32) ? buff[i | j] : ' ');
        }
        printf("%08x  %s  %s\n", i + add, out[0], out[1]);
    }
    puts("");
}
void head(char *a, int len) {
    printf("File name = %s, size =", a);
    int gb, mb, kb, b = len;
    kb = b >> 10, b &= 1023;
    mb = kb >> 10, kb &= 1023;
    gb = mb >> 10, mb &= 1023;
    if (gb) printf(" %dGB", gb);
    if (mb) printf(" %dMB", mb);
    if (kb) printf(" %dKB", kb);
    if (b) printf(" %dB", b);
    if (option) puts("");
}
int main(int argc, char **argv) {
    int len = 0;
    FILE *fp = 0;
    if (argc == 3) {
        sscanf(argv[2], "%d", &len);
        fp = fopen(argv[1], "r");
        if (fp == NULL) {
            puts("No such file!");
            exit(-1);
        }
        head(argv[1], len);
    } else if (argc == 2) {
        sprintf(buff, "hex %s $(ls -l %s | awk \'{print $5}\') ", argv[1], argv[1]);
        system(buff);
        return 0;
    } else if (argc == 1) {
        while (fgets(buff, 1000, stdin))
            hex(buff, strlen(buff) - 1);
        return 0;
    } else {
        exit(-1);
    }
    
    int flag = 0xFFFFFFFF ^ mask;
    char tmp[16];
    if (option == 1) {
        printf("Press Enter to go next page..\n");
        if (!fgets(tmp, 10, stdin))
            return 0;
    }

    for (int i = 0; i < len; i++) {
        buff[i & mask] = fgetc(fp);
        if ((i & mask) == mask) {
            hex(buff, maxn, i & flag);
            if (option == 1) {
                printf("\tPress Enter to go next page..\n");
                if (!fgets(tmp, 10, stdin))
                    return 0;
            }
        }
    }
    if (len & mask)
        hex(buff, len & mask, len & flag);

    return 0;
}
