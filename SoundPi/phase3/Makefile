# dragino lora testing
# Single lora testing app

CC=g++
CFLAGS=-c -Wall
LIBS=-lwiringPi

all: sendSigSessFin
	
sendSigSessFin: main.o
	$(CC) main.o  $(LIBS) -o sendSigSessFin

main.o: main.c
	$(CC) $(CFLAGS) main.c

clean:
	rm *.o sendSigSessFin
