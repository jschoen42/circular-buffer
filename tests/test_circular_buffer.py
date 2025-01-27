import pytest

from src.circular_buffer import CircularBuffer
from src.circular_buffer import CircularBufferMinimalSize, CircularBufferFull, CircularBufferEmpty

@pytest.mark.parametrize("size", [0, -10])
def test_CircularBuffer_minimal_size(size: int) -> None:
   with pytest.raises(CircularBufferMinimalSize) as excinfo:
      _ = CircularBuffer(size)
   assert excinfo.type is CircularBufferMinimalSize

@pytest.mark.parametrize("size", [10])
def test_CircularBuffer_normal_size(size: int) -> None:
   try:
        _ = CircularBuffer(size)
   except CircularBufferMinimalSize:
        pytest.fail("Unexpected MyError ..")

@pytest.mark.parametrize("size", [10])
def test_CircularBuffer_get_length(size: int) -> None:
   buf = CircularBuffer(size)
   assert len(buf) == size

def test_CircularBuffer_status_empty() -> None:
   buf = CircularBuffer(4)
   assert buf.empty() is True

def test_CircularBuffer_status_empty_full() -> None:
   buf = CircularBuffer(4)

   assert buf.empty() is True
   assert buf.full()  is False

   buf.write( 1 )
   buf.write( 2 )

   assert buf.full()  is False
   assert buf.empty() is False

   buf.write( 3 )

   assert buf.full()  is True
   assert buf.empty() is False

@pytest.mark.parametrize("size", [10])
def test_CircularBuffer_get_free(in_size: int) -> None:
   size: int = in_size

   buf = CircularBuffer(size)
   assert buf.free() == size-1

   buf.write( 1 )
   buf.write( 2 )

   assert buf.free() == size-3

def test_CircularBuffer_entries() -> None:
   buf = CircularBuffer(10)

   buf.write( 1 )
   buf.write( 2 )
   buf.write( 3 )
   buf.write( 4 )
   buf.write( 5 )

   assert buf.read() == 1
   assert buf.read() == 2
   assert buf.read() == 3
   assert buf.read() == 4
   assert buf.read() == 5

@pytest.mark.parametrize("size", [1, 10])
def test_CircularBuffer_dynamic(size: int) -> None:
   buf = CircularBuffer(size)

   for i in range(size-1):
      buf.write(i)

   with pytest.raises(CircularBufferFull) as excinfo:
      buf.write(size)
   assert excinfo.type is CircularBufferFull

   for i in range(size-1):
      assert buf.read() == i

   with pytest.raises(CircularBufferEmpty) as excinfo:
      buf.read()
   assert excinfo.type is CircularBufferEmpty


def test_CircularBuffer_raise_CircularBufferEmpty() -> None:
   buf = CircularBuffer(10)

   with pytest.raises(CircularBufferEmpty) as excinfo:
      buf.read()

   assert excinfo.type is CircularBufferEmpty

@pytest.mark.parametrize("size", [1, 10])
def test_CircularBuffer_raise_CircularBufferFull(size: int) -> None:
   buf = CircularBuffer(size)

   with pytest.raises(CircularBufferFull) as excinfo:
      for i in range(size):
         buf.write(i)

   assert excinfo.type is CircularBufferFull
