import asyncio
from typing import List, Tuple

import aiohttp


async def probe(
    session: aiohttp.ClientSession, method: str, url: str
) -> Tuple[str, str, int]:
    try:
        async with session.request(method, url, timeout=5) as resp:
            return method, url, resp.status
    except Exception:  # network errors etc.
        return method, url, -1  # use -1 as “failed”


async def run_wordlist_scan(
    base: str, wordlist: List[str]
) -> List[Tuple[str, str, int]]:
    methods = ["GET"]  # expand later
    connector = aiohttp.TCPConnector(limit_per_host=20)
    results: List[Tuple[str, str, int]] = []

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            asyncio.create_task(
                probe(session, m, f"{base.rstrip('/')}/{path.lstrip('/')}")
            )
            for path in wordlist
            for m in methods
        ]
        for finished in asyncio.as_completed(tasks):
            results.append(await finished)  # always inside the session

    return results
