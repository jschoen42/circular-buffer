"""
    © Jürgen Schoenemeyer, 04.03.2025 16:59

    tests/test_circular_buffer.py

    pytest -v
"""

import pytest

from src.helper.circular_buffer import CircularBuffer, CircularBufferEmptyError, CircularBufferFullError, CircularBufferMinimalSizeError

@pytest.mark.parametrize("size", [0, -10])
def test_circular_buffer_minimal_size(size: int) -> None:
    with pytest.raises(CircularBufferMinimalSizeError) as excinfo:
        _ = CircularBuffer(size)
    assert excinfo.type is CircularBufferMinimalSizeError

@pytest.mark.parametrize("size", [10])
def test_circular_buffer_normal_size(size: int) -> None:
    try:
        _ = CircularBuffer(size)
    except CircularBufferMinimalSizeError:
        pytest.fail("Unexpected MyError ..")

@pytest.mark.parametrize("size", [10])
def test_circular_buffer_get_length(size: int) -> None:
    buf = CircularBuffer(size)
    assert len(buf) == size

def test_circular_buffer_status_empty() -> None:
    buf = CircularBuffer(4)
    assert buf.empty() is True

def test_circular_buffer_status_empty_full() -> None:
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
def test_circular_buffer_get_free(size: int) -> None:
    buf = CircularBuffer(size)
    assert buf.free() == size-1

    buf.write( 1 )
    buf.write( 2 )

    assert buf.free() == size-3

def test_circular_buffer_entries() -> None:
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
def test_circular_buffer_dynamic(size: int) -> None:
    buf = CircularBuffer(size)

    for i in range(size-1):
        buf.write(i)

    with pytest.raises(CircularBufferFullError) as excinfo:
        buf.write(size)
    assert excinfo.type is CircularBufferFullError

    for i in range(size-1):
        assert buf.read() == i

    with pytest.raises(CircularBufferEmptyError) as excinfo:
        buf.read()
    assert excinfo.type is CircularBufferEmptyError


def test_circular_buffer_raise_CircularBufferEmptyError() -> None:  # noqa: N802
    buf = CircularBuffer(10)

    with pytest.raises(CircularBufferEmptyError) as excinfo:
        buf.read()

    assert excinfo.type is CircularBufferEmptyError

@pytest.mark.parametrize("size", [1, 10])
def test_circular_buffer_raise_CircularBufferFullError(size: int) -> None:  # noqa: N802
    buf = CircularBuffer(size)

    with pytest.raises(CircularBufferFullError) as excinfo:
        for i in range(size):
            buf.write(i)

    assert excinfo.type is CircularBufferFullError
