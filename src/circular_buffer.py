# https://www.kernel.org/doc/Documentation/circular-buffers.txt
# https://en.wikipedia.org/wiki/Circular_buffer

# https://www.youtube.com/watch?v=ebZB8dPrrog?t=210s

class CircularBufferMinimalSize(Exception):  # noqa: N818
    def __init__(self):
        super().__init__("Circular Buffer minimal size is 1")

class CircularBufferEmpty(Exception):  # noqa: N818
    def __init__(self):
        super().__init__("Circular Buffer ist empty")

class CircularBufferFull(Exception):  # noqa: N818
    def __init__(self, size: int):
        super().__init__(f"Circular Buffer limit {size} reached")
        self.size = size

# head: write - the point at which the producer inserts items into the buffer
# tail: read  - the point at which the consumer finds the next item in the buffer

class CircularBuffer:
    def __init__(self, size: int=100):
        self.size = size
        self.data = [None] * size
        self.tail = 0
        self.head = 0

        if size < 1:
            raise CircularBufferMinimalSize()

    def __len__(self):
        return self.size

    def __str__(self):
        return f"CircularBuffer: size={self.size}, free={self.free()}, tail={self.tail}, head={self.head}"

    def __repr__(self):
        return f"CircularBuffer: {self.size=}, {self.free=}, {self.tail=}, {self.head=}"

    def __iter__(self):
        return self

    def __next__(self) -> any:
        if self.tail == self.head:
            raise StopIteration

        value = self.data[self.tail]
        self.tail = (self.tail + 1) % self.size
        return value

    def full(self) -> bool:
        ptr = (self.head + 1) % self.size
        if ptr == self.tail:
            return True
        return False

    def empty(self) -> bool:
        return self.tail == self.head

    def free(self) -> int:
        return((self.tail - self.head + self.size - 1) % self.size)

    def write(self, value: any) -> None:
        ptr = (self.head + 1) % self.size
        if ptr == self.tail:
            raise CircularBufferFull( self.size-1 )

        self.data[self.head] = value
        self.head = ptr

    def read(self) -> any:
        if self.tail == self.head:
            raise CircularBufferEmpty

        value = self.data[self.tail]
        self.tail = (self.tail + 1) % self.size
        return value

    def reset(self) -> None:
        self.tail = 0
        self.head = 0

