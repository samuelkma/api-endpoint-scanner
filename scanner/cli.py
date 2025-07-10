import asyncio
import pathlib

import click

from scanner.core import run_wordlist_scan

WORDLIST = (
    pathlib.Path(__file__).with_suffix("").with_name("..").resolve()
    / "data/wordlists/common.txt"
)


@click.command()
@click.argument("target")
def main(target: str):
    with open(WORDLIST) as f:
        words = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]  # break list-comp over multiple lines
    hits = asyncio.run(run_wordlist_scan(target, words))
    for m, url, status in hits:
        if status not in (404,):
            print(f"{m:<4} {url:<60} {status}")


if __name__ == "__main__":
    main()
