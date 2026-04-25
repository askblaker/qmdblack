from qmdblack.core import format_qmd

UNFORMATTED = """\
# My notebook

Some prose.

```{python}
x=1+2
y   =   x*3
```

More prose.
"""

FORMATTED = """\
# My notebook

Some prose.

```{python}
x = 1 + 2
y = x * 3
```

More prose.
"""

WITH_DIRECTIVES = """\
```{python}
#| echo: false
#| warning: false
x=1+2
```
"""

WITH_DIRECTIVES_FORMATTED = """\
```{python}
#| echo: false
#| warning: false
x = 1 + 2
```
"""

MULTIPLE_BLOCKS = """\
```{python}
a=1
```

```{python}
b=2
```
"""

MULTIPLE_BLOCKS_FORMATTED = """\
```{python}
a = 1
```

```{python}
b = 2
```
"""

NON_PYTHON_BLOCK = """\
```{r}
x <- 1
```

```{python}
y=2
```
"""

NON_PYTHON_BLOCK_FORMATTED = """\
```{r}
x <- 1
```

```{python}
y = 2
```
"""


def test_basic_formatting():
    assert format_qmd(UNFORMATTED) == FORMATTED


def test_directives_preserved():
    assert format_qmd(WITH_DIRECTIVES) == WITH_DIRECTIVES_FORMATTED


def test_multiple_blocks():
    assert format_qmd(MULTIPLE_BLOCKS) == MULTIPLE_BLOCKS_FORMATTED


def test_non_python_block_unchanged():
    assert format_qmd(NON_PYTHON_BLOCK) == NON_PYTHON_BLOCK_FORMATTED


def test_already_formatted_unchanged():
    assert format_qmd(FORMATTED) == FORMATTED


def test_directives_only_block_unchanged():
    source = """\
```{python}
#| echo: false
```
"""
    assert format_qmd(source) == source


def test_line_length():
    source = """\
```{python}
x = some_long_func(argument_one, argument_two, argument_three, argument_four)
```
"""
    result = format_qmd(source, line_length=50)
    # black should have wrapped the line
    assert max(len(line) for line in result.splitlines()) <= 50
