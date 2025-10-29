# Module: `src/core/ssl/PoC_SSL.py`

Import path: `src.core.ssl.PoC_SSL`

## Module docstring

No docstring provided.

## Basic import example

```python
from src.core.ssl.PoC_SSL import <symbol>
# <symbol> can be a function or class from this module
```

## Functions

### `main_server(HandlerClass=SecureHTTPRequestHandler, ServerClass=SecureHTTPServer)`

No docstring provided.

```python
from src.core.ssl.PoC_SSL import main_server
result = main_server()
```

## Classes

### `SecureHTTPServer`

No docstring provided.

```python
from src.core.ssl.PoC_SSL import SecureHTTPServer
obj = SecureHTTPServer(self=..., server_address=..., HandlerClass=...)
# Call a method (if available):
obj.shutdown_request(request=...)
```

#### Methods

- `shutdown_request(self, request)`
  - No docstring provided.

### `SecureHTTPRequestHandler`

No docstring provided.

```python
from src.core.ssl.PoC_SSL import SecureHTTPRequestHandler
obj = SecureHTTPRequestHandler()
# Call a method (if available):
obj.setup()
```

#### Methods

- `setup(self)`
  - No docstring provided.
