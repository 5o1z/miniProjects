# Variables
TARGET = phonebook
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g

SRCS = main.c utils.c handler.c
OBJS = $(SRCS:.c=.o)
DEPS = phonebook.h

# Default target
all: $(TARGET)

# Linking
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

# Compiling
%.o: %.c $(DEPS)
	$(CC) $(CFLAGS) -c $< -o $@

# Cleanup
clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
