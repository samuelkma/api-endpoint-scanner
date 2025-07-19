import asyncio
from typing import List, Tuple

import aiohttp

Result = Tuple[str, str, int]  # (method, url, status)


async def probe(session: aiohttp.ClientSession, method: str, url: str) -> Result:
    try:
        async with session.request(method, url, timeout=5) as resp:
            return method, url, resp.status
    except Exception:  # network errors etc.
        return method, url, -1  # use -1 as “failed”


async def run_wordlist_scan(base: str, wordlist: List[str]) -> List[Result]:
    methods = ["GET"]  # expand later
    connector = aiohttp.TCPConnector(limit_per_host=20)
    results: List[Result] = []
    # gather results as they finish, to avoid waiting for all tasks
    # and to handle network errors gracefully

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
