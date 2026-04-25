import difflib
import sys
from importlib.metadata import version as _package_version
from pathlib import Path

import click

from .core import format_qmd


def _collect_files(src: tuple[Path, ...]) -> list[Path]:
    files = []
    for path in src:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.qmd")))
        else:
            files.append(path)
    return files


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=_package_version("qmdblack"))
@click.argument("src", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--check",
    is_flag=True,
    help="Don't write files, just return status. Exit 1 if files would be reformatted.",
)
@click.option(
    "--diff",
    is_flag=True,
    help="Don't write files, show a diff of what would change.",
)
@click.option(
    "-l",
    "--line-length",
    default=88,
    show_default=True,
    help="How many characters per line to allow.",
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Suppress 'All good' messages. Only report files that would be reformatted.",
)
def main(
    src: tuple[Path, ...],
    check: bool,
    diff: bool,
    line_length: int,
    quiet: bool,
) -> None:
    """Format Python code blocks in Quarto Markdown (.qmd) files."""
    if not src:
        click.echo("No files provided. Use --help for usage.", err=True)
        sys.exit(1)

    files = _collect_files(src)

    if not files:
        click.echo("No .qmd files found.", err=True)
        sys.exit(1)

    would_reformat = False

    for path in files:
        original = path.read_text(encoding="utf-8")
        formatted = format_qmd(original, line_length=line_length)

        if formatted == original:
            if not quiet:
                click.echo(f"All good: {path}")
            continue

        would_reformat = True

        if diff:
            delta = difflib.unified_diff(
                original.splitlines(keepends=True),
                formatted.splitlines(keepends=True),
                fromfile=f"{path} (original)",
                tofile=f"{path} (reformatted)",
            )
            click.echo("".join(delta), nl=False)
        elif check:
            click.echo(f"Would reformat: {path}")
        else:
            path.write_text(formatted, encoding="utf-8")
            click.echo(f"Reformatted: {path}")

    if check and would_reformat:
        sys.exit(1)
