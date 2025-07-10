# tests/test_core.py

import pytest

from scanner.core import run_wordlist_scan


@pytest.mark.asyncio
async def test_finds_known_endpoint():
    hits = await run_wordlist_scan(
        "http://127.0.0.1:8000",
        ["api/home", "bogus"],
    )
    assert ("GET", "http://127.0.0.1:8000/api/home", 200) in hits
