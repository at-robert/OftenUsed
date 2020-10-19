CROSS =
CC = $(CROSS)gcc
AR = $(CROSS)ar
STRIP = $(CROSS)strip
LDFLAGS +=


EXEC = c_pthread_test
OBJS = c_pthread_test.o child_thread.o
LOCAL_LDFLAGS := -lpthread

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LIBM) $(LDLIBS) $(LIBGCC) $(LOCAL_LDFLAGS) -lm

clean:
	-rm -f $(EXEC) *.elf *.gdb *.o
