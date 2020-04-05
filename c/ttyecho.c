/*
Program for linux systems. Used in situations where output of a command running on one terminal is desired on another open terminal
*/
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <string.h>
#include <unistd.h>

void print_help(char *prog_name) {
        printf("Usage: %s DEVNAME COMMAND\n", prog_name);
        printf("Usage: Will require 'sudo' to run if the executable is not setuid root\n");
        exit(1);
}

int main (int argc, char *argv[]) {
    char *cmd;
    int i, fd;
    int mem_len;
    if (argc < 3) {
        print_help(argv[0]);
    }
    fd = open(argv[1],O_RDWR);
    if(fd == -1) {
        perror("open DEVICE");
        exit(1);
    }
    mem_len = 0;
    for ( i = 2; i < argc; i++ ) {
        mem_len += strlen(argv[i]) + 2;
        if ( i > 2 ) {
            cmd = realloc(cmd, mem_len);
        } else {
            cmd = malloc(mem_len);
        }

        strcat(cmd, argv[i]);
        strcat(cmd, " ");
    }
	strcat(cmd, "\n");
	for (i = 0 ; cmd[i]; i++)
		ioctl(fd, TIOCSTI, cmd+i);
    close(fd);
    free(cmd);
    return 0;
}
