## src.fasttrack.autopwn

### Functions

- **do_autopwn**

  ```python
def do_autopwn(): ...
  ```

- **launch**

  ```python
def launch(): ...
  ```

  here we cant use the path for metasploit via setcore.meta_path. If the full path is specified it breaks
  database support for msfconsole for some reason. reported this as a bug, may be fixed soon... until then
  if path variables aren't set for msfconsole this will break, even if its specified in set_config

- **prep**

  ```python
def prep(database, ranges): ...
  ```
