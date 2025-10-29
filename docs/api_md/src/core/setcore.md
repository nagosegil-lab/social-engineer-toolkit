## src.core.setcore

### Functions

- **applet_choice**

  ```python
def applet_choice(): ...
  ```

- **bin2ip**

  ```python
def bin2ip(b): ...
  ```

- **capture**

  ```python
def capture(func, *args, **kwargs): ...
  ```

  Capture the output of func when called with the given arguments.
  The function output includes any exception raised. capture returns
  a tuple of (function result, standard output, standard error).

- **check_backbox**

  ```python
def check_backbox(): ...
  ```

- **check_config**

  ```python
def check_config(param): ...
  ```

- **check_kali**

  ```python
def check_kali(): ...
  ```

- **check_length**

  ```python
def check_length(choice, max): ...
  ```

- **check_options**

  ```python
def check_options(option): ...
  ```

- **check_os**

  ```python
def check_os(): ...
  ```

- **check_ports**

  ```python
def check_ports(filename, port): ...
  ```

- **cleanup_routine**

  ```python
def cleanup_routine(): ...
  ```

- **copyfolder**

  ```python
def copyfolder(sourcePath, destPath): ...
  ```

- **custom_template**

  ```python
def custom_template(): ...
  ```

- **date_time**

  ```python
def date_time(): ...
  ```

- **debug_msg**

  ```python
def debug_msg(currentModule, message, msgType): ...
  ```

- **dec2bin**

  ```python
def dec2bin(n, d=…): ...
  ```

- **definepath**

  ```python
def definepath(): ...
  ```

- **detect_public_ip**

  ```python
def detect_public_ip(): ...
  ```

  Helper function to auto-detect our public IP(v4) address.

- **encryptAES**

  ```python
def encryptAES(secret, data): ...
  ```

- **exit_set**

  ```python
def exit_set(): ...
  ```

- **fetch_template**

  ```python
def fetch_template(): ...
  ```

- **generate_powershell_alphanumeric_payload**

  ```python
def generate_powershell_alphanumeric_payload(payload, ipaddr, port, payload2): ...
  ```

- **generate_random_string**

  ```python
def generate_random_string(low, high): ...
  ```

- **generate_shellcode**

  ```python
def generate_shellcode(payload, ipaddr, port): ...
  ```

- **get_sql_port**

  ```python
def get_sql_port(host): ...
  ```

- **get_version**

  ```python
def get_version(): ...
  ```

- **grab_ipaddress**

  ```python
def grab_ipaddress(): ...
  ```

- **help_menu**

  ```python
def help_menu(): ...
  ```

- **input**

  ```python
def input(string): ...
  ```

- **ip2bin**

  ```python
def ip2bin(ip): ...
  ```

- **is_valid_ip**

  ```python
def is_valid_ip(ip): ...
  ```

- **is_valid_ipv4**

  ```python
def is_valid_ipv4(ip): ...
  ```

- **is_valid_ipv6**

  ```python
def is_valid_ipv6(ip): ...
  ```

  Validates IPv6 addresses.

- **java_applet_attack**

  ```python
def java_applet_attack(website, port, directory): ...
  ```

- **kill_proc**

  ```python
def kill_proc(port, flag): ...
  ```

- **log**

  ```python
def log(error): ...
  ```

- **menu_back**

  ```python
def menu_back(): ...
  ```

- **meta_database**

  ```python
def meta_database(): ...
  ```

- **meta_path**

  ```python
def meta_path(): ...
  ```

- **metasploit_shellcode**

  ```python
def metasploit_shellcode(payload, ipaddr, port): ...
  ```

- **mod_name**

  ```python
def mod_name(): ...
  ```

- **module_reload**

  ```python
def module_reload(module): ...
  ```

- **powershell_encodedcommand**

  ```python
def powershell_encodedcommand(ps_attack): ...
  ```

- **print_error**

  ```python
def print_error(message): ...
  ```

- **print_info**

  ```python
def print_info(message): ...
  ```

- **print_info_spaces**

  ```python
def print_info_spaces(message): ...
  ```

- **print_status**

  ```python
def print_status(message): ...
  ```

- **print_warning**

  ```python
def print_warning(message): ...
  ```

- **printCIDR**

  ```python
def printCIDR(c): ...
  ```

- **return_continue**

  ```python
def return_continue(): ...
  ```

- **set_check**

  ```python
def set_check(): ...
  ```

- **setdir**

  ```python
def setdir(): ...
  ```

- **setprompt**

  ```python
def setprompt(category, text): ...
  ```

- **shellcode_replace**

  ```python
def shellcode_replace(ipaddr, port, shellcode): ...
  ```

- **show_banner**

  ```python
def show_banner(define_version, graphic): ...
  ```

- **show_graphic**

  ```python
def show_graphic(): ...
  ```

- **site_cloner**

  ```python
def site_cloner(website, exportpath, *args): ...
  ```

- **socket_listener**

  ```python
def socket_listener(port): ...
  ```

- **start_web_server**

  ```python
def start_web_server(directory): ...
  ```

- **start_web_server_unthreaded**

  ```python
def start_web_server_unthreaded(directory): ...
  ```

- **tail**

  ```python
def tail(filename): ...
  ```

- **teensy_pde_generator**

  ```python
def teensy_pde_generator(attack_method): ...
  ```

- **update_options**

  ```python
def update_options(option): ...
  ```

- **update_set**

  ```python
def update_set(): ...
  ```

- **upx**

  ```python
def upx(path_to_file): ...
  ```

- **validate_ip**

  ```python
def validate_ip(address): ...
  ```

  Validates that a given string is an IPv4 dotted quad.

- **validateCIDRBlock**

  ```python
def validateCIDRBlock(b): ...
  ```

- **windows_root**

  ```python
def windows_root(): ...
  ```

- **yesno_prompt**

  ```python
def yesno_prompt(category, text): ...
  ```

### Classes

- **create_menu**
