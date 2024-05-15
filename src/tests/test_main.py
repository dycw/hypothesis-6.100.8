from __future__ import annotations

from hypothesis_6.100.8 import __version__


def test_main() -> None:
    assert isinstance(__version__, str)
