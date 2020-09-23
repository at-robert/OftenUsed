CROSS =
CC = $(CROSS)gcc
AR = $(CROSS)ar
STRIP = $(CROSS)strip
LDFLAGS +=


EXEC = amtran_test_uart
OBJS = amtran_test_uart.o 

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LIBM) $(LDLIBS) $(LIBGCC) -lm

clean:
	-rm -f $(EXEC) *.elf *.gdb *.o
