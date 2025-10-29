## src.core.webserver

### Functions

- **start_server**

  ```python
def start_server(web_port, path): ...
  ```

- **stop_server**

  ```python
def stop_server(web_port): ...
  ```

### Classes

- **StoppableHttpRequestHandler**

  http request handler with QUIT stopping the server

  - Methods

    - `do_POST(self)`
    - `do_QUIT(self)`
      send 200 OK response, and set server.stop to True
    - `send_head(self)`
      Common code for GET and HEAD commands.

      This sends the response code and MIME headers.

      Return value is either a file object (which has to be copied
      to the outputfile by the caller unless the command was HEAD,
      and must be closed by the caller under all circumstances), or
      None, in which case the caller has nothing further to do.

- **StoppableHttpServer**

  http server that reacts to self.stop flag

  - Methods

    - `serve_forever(self)`
      Handle one request at a time until stopped.
