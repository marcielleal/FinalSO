all: 
	gcc  `pkg-config gtk+-3.0 --cflags` display-manager.c  pam.c -lpam -lpam_misc -o display-manager `pkg-config gtk+-3.0 --libs` -lpthread
