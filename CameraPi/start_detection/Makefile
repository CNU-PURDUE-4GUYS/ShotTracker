# dragino lora testing
# Single lora testing app

CC=g++
CFLAGS=-c -Wall
LIBS=-lwiringPi

all: lora

lora: main.o
	$(CC) main.o  $(LIBS) -o lora

main.o: main.c
	$(CC) $(CFLAGS) main.c

clean:
	rm *.o lora
