# qmdblack

Format Python code blocks in [Quarto Markdown](https://quarto.org/) (`.qmd`) files using [Black](https://github.com/psf/black).

Quarto cell option directives (`#|` lines) are preserved as-is at the top of each block.

## Installation

```bash
pip install qmdblack
```

## Usage

```bash
# Format files in-place
qmdblack notebook.qmd

# Check without writing (exit 1 if any file would change)
qmdblack --check notebook.qmd

# Show a diff without writing
qmdblack --diff notebook.qmd

# Custom line length (default: 88)
qmdblack -l 100 notebook.qmd

# Multiple files
qmdblack *.qmd
```

## Example

Before:

````markdown
```{python}
#| echo: false
x=1+2
y   =   x*3
print(   y   )
```
````

After:

````markdown
```{python}
#| echo: false
x = 1 + 2
y = x * 3
print(y)
```
````
