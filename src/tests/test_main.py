from __future__ import annotations

from string import ascii_letters
from typing import cast

from hypothesis import assume, given
from hypothesis.errors import InvalidArgument
from hypothesis.extra.numpy import Shape, array_shapes, arrays
from hypothesis.strategies import (
    DataObject,
    DrawFn,
    SearchStrategy,
    composite,
    data,
    integers,
    none,
    nothing,
    text,
)
from numpy import ndarray, str_
from numpy.typing import NDArray


def draw_text(
    alphabet: str, /, *, min_size: int = 0, max_size: int | None = None
) -> SearchStrategy[str]:
    """Draw from a text-generating strategy."""
    return text(alphabet, min_size=min_size, max_size=max_size)


def text_ascii(*, min_size: int, max_size: int | None) -> SearchStrategy[str]:
    """Strategy for generating ASCII text."""
    return draw_text(ascii_letters, min_size=min_size, max_size=max_size)


@composite
def str_arrays(
    draw: DrawFn, /, *, shape: Shape | None, min_size: int, max_size: int | None
) -> NDArray[str]:
    elements = text_ascii(min_size=min_size, max_size=max_size)
    strategy = cast(
        SearchStrategy[NDArray[str_]],
        arrays(object, shape, elements=elements, fill=nothing(), unique=False),
    )
    return draw(strategy)


@given(
    data=data(),
    shape=array_shapes(),
    min_size=integers(0, 100),
    max_size=integers(0, 100) | none(),
)
def test_main(
    *, data: DataObject, shape: Shape, min_size: int, max_size: int | None
) -> None:
    try:
        array = data.draw(str_arrays(shape=shape, min_size=min_size, max_size=max_size))
    except InvalidArgument:
        _ = assume(condition=False)
        raise
    assert isinstance(array, ndarray)
