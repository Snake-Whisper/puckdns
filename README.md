# puck-dns-api
Python API for the great free DNS Service "PUCK" (http://puck.nether.net/dns)

Usage:
---

```python
import puckdns
from sys import exit

# initialise puck dns class
puck = puckdns.API()

# login with ur credentials
try:
  puck.login ("username", "password")
except AssertionError:
  print ("[FATAL] Idiot, false login credentials. Or something else.")
  print ("[FATAL] Login failed. Please try again (later).")
  exit (-1)

# Do something
```

