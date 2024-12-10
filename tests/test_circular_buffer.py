import pytest

from src.circular_buffer import CircularBuffer
from src.circular_buffer import CircularBufferFull, CircularBufferEmpty

def test_CircularBuffer_get_length() -> None:
   size: int = 10

   buf = CircularBuffer(size)
   assert len(buf) == 10

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

def test_CircularBuffer_get_free() -> None:
   size: int = 10

   buf = CircularBuffer(size)
   assert buf.free() == size-1

   buf.write( 1 )
   buf.write( 2 )

   assert buf.free() == size-1-2

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


def test_CircularBuffer_raise_CircularBufferEmpty() -> None:
   buf = CircularBuffer(10)

   with pytest.raises(CircularBufferEmpty) as excinfo:
      buf.read()

   assert excinfo.type is CircularBufferEmpty

def test_CircularBuffer_raise_CircularBufferFull() -> None:
   buf = CircularBuffer(4)

   with pytest.raises(CircularBufferFull) as excinfo:
      buf.write(1)
      buf.write(2)
      buf.write(3)
      buf.write(4)

   assert excinfo.type is CircularBufferFull
