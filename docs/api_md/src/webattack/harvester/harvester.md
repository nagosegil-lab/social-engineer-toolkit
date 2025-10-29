## src.webattack.harvester.harvester

### Functions

- **htc**

  ```python
def htc(m): ...
  ```

- **run**

  ```python
def run(): ...
  ```

- **ssl_server**

  ```python
def ssl_server(HandlerClass=…, ServerClass=…): ...
  ```

- **urldecode**

  ```python
def urldecode(url): ...
  ```

### Classes

- **SecureHTTPServer**

  - Methods

    - `shutdown_request(self, request)`

- **SETHandler**

  - Methods

    - `do_GET(self)`
    - `do_POST(self)`
    - `setup(self)`

- **ThreadedHTTPServer**

  Handle requests in a separate thread.
