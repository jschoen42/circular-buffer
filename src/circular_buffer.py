class CircularBufferFull(Exception):  # noqa: N818
    pass

class CircularBufferEmpty(Exception):  # noqa: N818
    pass

class CircularBuffer:
    def __init__(self, size: int=100):
        self.size = size
        self.data = [None] * size
        self.read_ptr  = 0
        self.write_ptr = 0

    def __len__(self):
        return self.size

    def __str__(self):
        return f"CircularBuffer: free={self.free()}, size={self.size}, read_ptr={self.read_ptr}, write_ptr={self.write_ptr}"

    def __repr__(self):
        return f"CircularBuffer: {self.free=}, {self.size=}, {self.read_ptr=}, {self.write_ptr=}"

    def __iter__(self):
        return self

    def __next__(self) -> any:
        if self.read_ptr == self.write_ptr:
            raise StopIteration

        value = self.data[self.read_ptr]
        self.read_ptr = (self.read_ptr + 1) % self.size
        return value

    def full(self) -> bool:
        ptr = (self.write_ptr + 1) % self.size
        if ptr == self.read_ptr:
            return True
        return False

    def empty(self) -> bool:
        return self.read_ptr == self.write_ptr

    def free(self) -> int:
        return((self.read_ptr - self.write_ptr + self.size - 1) % self.size)

    def write(self, value: any) -> None:
        ptr = (self.write_ptr + 1) % self.size
        if ptr == self.read_ptr:
            raise CircularBufferFull

        self.data[self.write_ptr] = value
        self.write_ptr = ptr

    def read(self) -> any:
        if self.read_ptr == self.write_ptr:
            raise CircularBufferEmpty

        value = self.data[self.read_ptr]
        self.read_ptr = (self.read_ptr + 1) % self.size
        return value

    def reset(self) -> None:
        self.read_ptr = 0
        self.write_ptr = 0

