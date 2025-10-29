## src.core.minifakedns

SET core PyFakeMiniDNS server implementation.

Slightly modified implementation of Francisco Santos's PyfakeminiDNS
script designed to run as a thread and handle various additional
system configuration tasks, if necessary in the running environment,
along with a few implementation considerations specifically for SET.

### Functions

- **start_dns_server**

  ```python
def start_dns_server(reply_ip): ...
  ```

  Helper function, intended to be called from other modules.

  Args:
      reply_ip (string): IPv4 address in dotted quad notation to use in all answers.

- **stop_dns_server**

  ```python
def stop_dns_server(): ...
  ```

  Helper function, intended to be called from other modules.

### Classes

- **DNSQuery**

  A DNS query (that can be parsed as binary data).

  See original for reference, but note there have been changes:
      https://code.activestate.com/recipes/491264-mini-fake-dns-server/
  Among the changes are variables names that have been translated
  to English from their original Spanish.

  - Methods

    - `response(self, ip)`
      Construct a DNS reply packet with a given IP address.

      TODO: This responds incorrectly to EDNS queries that make use
            of the OPT pseudo-record type. Specifically, the pointer
            wrong because we do not check the length of the original
            query we received. Instead, we should note the length of
            the original packet until the end of the first question,
            and truncate (i.e., drop, ignore) the remainder.

            For now, what this actually means is that testing this
            server using a recent version of `dig(1)` will fail
            unless you use the `+noedns` query option. For example:

                dig @127.0.0.1 example.com +noedns

            Simpler or older DNS utilities such as `host(1)` are
            probably going to work.

      Args:
          ip (string): IP address to respond with.

- **MiniFakeDNS**

  The MiniFakeDNS server, written to be run as a Python Thread.

  - Methods

    - `cede_to_systemd_resolved(self)`
      Helper function to cede system configuration back to systemd-resolved
      after we have usurped control over DNS configuration away from it.
    - `cleanup(self)`
    - `run(self)`
    - `stop(self)`
      Signals to the DNS server thread to stop.
    - `usurp_systemd_resolved(self)`
      Helper function to get systemd-resolved out of the way when it
      is listening on 127.0.0.1:53 and we are trying to run SET's
      own DNS server.
