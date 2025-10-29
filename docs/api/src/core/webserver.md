# Module: `src/core/webserver.py`

Import path: `src.core.webserver`

## Module docstring

No docstring provided.

## Basic import example

```python
from src.core.webserver import <symbol>
# <symbol> can be a function or class from this module
```

## Functions

### `stop_server(web_port)`

No docstring provided.

```python
from src.core.webserver import stop_server
result = stop_server(web_port=...)
```

### `start_server(web_port, path)`

No docstring provided.

```python
from src.core.webserver import start_server
result = start_server(web_port=..., path=...)
```

## Classes

### `StoppableHttpRequestHandler`

http request handler with QUIT stopping the server

```python
from src.core.webserver import StoppableHttpRequestHandler
obj = StoppableHttpRequestHandler()
# Call a method (if available):
obj.do_QUIT()
```

#### Methods

- `do_QUIT(self)`
  - send 200 OK response, and set server.stop to True

- `do_POST(self)`
  - No docstring provided.

- `send_head(self)`
  - Common code for GET and HEAD commands.

This sends the response code and MIME headers.

Return value is either a file object (which has to be copied
to the outputfile by the caller unless the command was HEAD,
and must be closed by the caller under all circumstances), or
None, in which case the caller has nothing further to do.

### `StoppableHttpServer`

http server that reacts to self.stop flag

```python
from src.core.webserver import StoppableHttpServer
obj = StoppableHttpServer()
# Call a method (if available):
obj.serve_forever()
```

#### Methods

- `serve_forever(self)`
  - Handle one request at a time until stopped.
