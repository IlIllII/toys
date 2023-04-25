CC = cl
CFLAGS = /O2 /Qfast_transcendentals /Qpar /Qpar-report:1 /Qpar-report:2 /Qvec-report:1 /Qvec-report:2 /Gr /arch:AVX2
TARGET = matmul
OBJECTS = matmul.obj

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJECTS)

$(OBJECTS): matmul.c
	$(CC) $(CFLAGS) -c matmul.c

clean:
	del $(OBJECTS) $(TARGET).exe
