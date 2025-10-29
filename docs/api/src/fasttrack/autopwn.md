# Module: `src/fasttrack/autopwn.py`

Import path: `src.fasttrack.autopwn`

## Module docstring

No docstring provided.

## Basic import example

```python
from src.fasttrack.autopwn import <symbol>
# <symbol> can be a function or class from this module
```

## Functions

### `prep(database, ranges)`

No docstring provided.

```python
from src.fasttrack.autopwn import prep
result = prep(database=..., ranges=...)
```

### `launch()`

here we cant use the path for metasploit via setcore.meta_path. If the full path is specified it breaks
database support for msfconsole for some reason. reported this as a bug, may be fixed soon... until then
if path variables aren't set for msfconsole this will break, even if its specified in set_config

```python
from src.fasttrack.autopwn import launch
result = launch()
```

### `do_autopwn()`

No docstring provided.

```python
from src.fasttrack.autopwn import do_autopwn
result = do_autopwn()
```
