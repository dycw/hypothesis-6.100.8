from __future__ import annotations

from string import ascii_letters
from typing import TYPE_CHECKING

from hypothesis import assume, given
from hypothesis.errors import InvalidArgument
from hypothesis.extra.numpy import Shape, array_shapes, arrays
from hypothesis.strategies import (
    DataObject,
    SearchStrategy,
    data,
    integers,
    none,
    nothing,
    text,
)
from numpy import ndarray, str_

if TYPE_CHECKING:
    from numpy.typing import NDArray


def str_arrays(
    *, shape: Shape, min_size: int, max_size: int | None
) -> SearchStrategy[NDArray[str_]]:
    elements = text(ascii_letters, min_size=min_size, max_size=max_size)
    return arrays(object, shape, elements=elements, fill=nothing(), unique=False)


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
