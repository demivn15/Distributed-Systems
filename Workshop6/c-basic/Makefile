CC = gcc
CFLAGS = -Wall $(shell pkg-config --cflags librabbitmq)
LDLIBS = $(shell pkg-config --libs librabbitmq)

all: c_producer c_consumer

c_producer: c_producer.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

c_consumer: c_consumer.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

clean:
	rm -f c_producer c_consumer