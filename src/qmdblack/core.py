import re

import black

_FENCE_OPEN = re.compile(r"^```\{python\}[^\n]*$")
_FENCE_CLOSE = re.compile(r"^```\s*$")


def format_qmd(source: str, line_length: int = 88) -> str:
    lines = source.splitlines(keepends=True)
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if _FENCE_OPEN.match(line.rstrip("\n")):
            result.append(line)
            i += 1

            directives: list[str] = []
            code_lines: list[str] = []
            past_directives = False

            while i < len(lines) and not _FENCE_CLOSE.match(lines[i].rstrip("\n")):
                bl = lines[i]
                if not past_directives and bl.startswith("#|"):
                    directives.append(bl)
                else:
                    past_directives = True
                    code_lines.append(bl)
                i += 1

            closing = lines[i] if i < len(lines) else "```\n"
            i += 1

            code = "".join(code_lines)
            if code.strip():
                mode = black.Mode(line_length=line_length)
                try:
                    code = black.format_str(code, mode=mode)
                except black.InvalidInput:
                    pass

            result.extend(directives)
            if code:
                result.append(code if code.endswith("\n") else code + "\n")
            result.append(closing)
        else:
            result.append(line)
            i += 1

    return "".join(result)
