from __future__ import annotations

from hypothesis_6_100_8 import __version__


def test_main() -> None:
    assert isinstance(__version__, str)
