# Module: `modules/ratte_only_module.py`

## Module docstring

No docstring provided.

## Importing by file path

```python
import importlib.util
spec = importlib.util.spec_from_file_location("ratte_only_module", "/workspace/modules/ratte_only_module.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
# Now use: mod.<symbol>(...) or mod.<Class>(...)
```

## Functions

### `ratte_listener_start(port)`

No docstring provided.

```python
# After running the import-by-path snippet above:
result = mod.ratte_listener_start(port=...)
```

### `prepare_ratte(ipaddr, ratteport, persistent, customexe)`

No docstring provided.

```python
# After running the import-by-path snippet above:
result = mod.prepare_ratte(ipaddr=..., ratteport=..., persistent=..., customexe=...)
```

### `main()`

No docstring provided.

```python
# After running the import-by-path snippet above:
result = mod.main()
```
