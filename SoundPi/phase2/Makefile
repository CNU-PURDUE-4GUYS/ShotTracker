# dragino lora testing
# Single lora testing app

CC=g++
CFLAGS=-c -Wall
LIBS=-lwiringPi

all: sendSigCapture 
	
sendSigCapture: main.o
	$(CC) main.o  $(LIBS) -o sendSigCapture

main.o: main.c
	$(CC) $(CFLAGS) main.c

clean:
	rm *.o sendSigCapture 
