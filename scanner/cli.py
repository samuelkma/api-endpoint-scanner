import asyncio
import pathlib

import click
import rich.console

from scanner.core import run_wordlist_scan

WORDLIST = (
    pathlib.Path(__file__).with_suffix("").with_name("..").resolve()
    / "data/wordlists/common.txt"
)
console = rich.console.Console()


@click.command()
@click.argument("target")
# option to show all results, including 404s and -1s
@click.option("--show-fails", is_flag=True, help="Also display 404 / -1 results")
def main(target: str, show_fails: bool):
    with open(WORDLIST) as f:
        words = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]  # break list-comp over multiple lines
    hits = asyncio.run(run_wordlist_scan(target, words))
    for m, url, status in hits:
        is_hit = status not in (404, -1)
        if is_hit or show_fails:
            colour = (
                "green"
                if 200 <= status < 300
                else "yellow" if 300 <= status < 400 or status == 403 else "red"
            )
            console.print(f"{m:<4} {url:<60} {status}", style=colour)

    total = len(hits)
    discovered = sum(1 for _, _, s in hits if s not in (404, -1))
    console.print(
        f"\n[bold]Found[/bold] {discovered} valid endpoints out of {total} probes"
    )


if __name__ == "__main__":
    main()
