# Module: `src/webattack/harvester/harvester.py`

Import path: `src.webattack.harvester.harvester`

## Module docstring

No docstring provided.

## Basic import example

```python
from src.webattack.harvester.harvester import <symbol>
# <symbol> can be a function or class from this module
```

## Functions

### `htc(m)`

No docstring provided.

```python
from src.webattack.harvester.harvester import htc
result = htc(m=...)
```

### `urldecode(url)`

No docstring provided.

```python
from src.webattack.harvester.harvester import urldecode
result = urldecode(url=...)
```

### `run()`

No docstring provided.

```python
from src.webattack.harvester.harvester import run
result = run()
```

### `ssl_server(HandlerClass=SETHandler, ServerClass=SecureHTTPServer)`

No docstring provided.

```python
from src.webattack.harvester.harvester import ssl_server
result = ssl_server()
```

## Classes

### `SETHandler`

No docstring provided.

```python
from src.webattack.harvester.harvester import SETHandler
obj = SETHandler()
# Call a method (if available):
obj.setup()
```

#### Methods

- `setup(self)`
  - No docstring provided.

- `do_GET(self)`
  - No docstring provided.

- `do_POST(self)`
  - No docstring provided.

### `ThreadedHTTPServer`

Handle requests in a separate thread.

```python
from src.webattack.harvester.harvester import ThreadedHTTPServer
obj = ThreadedHTTPServer()
# Call a method (if available):
# (no public methods detected)
```

### `SecureHTTPServer`

No docstring provided.

```python
from src.webattack.harvester.harvester import SecureHTTPServer
obj = SecureHTTPServer(self=..., server_address=..., HandlerClass=...)
# Call a method (if available):
obj.shutdown_request(request=...)
```

#### Methods

- `shutdown_request(self, request)`
  - No docstring provided.
