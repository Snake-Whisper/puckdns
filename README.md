# puck-dns-api

Python API for the great free DNS Service "PUCK" (http://puck.nether.net/dns)

---
## Login

```python
import puckdns
from sys import exit

# initialise puck dns class
puck = puckdns.API()

# login with ur credentials
try:
  puck.login ("username", "password")
except LoginFailed:
  print ("[FATAL] Idiot, false login credentials. Or something else.")
  print ("[FATAL] Login failed. Please try again (later).")
  exit (-1)

```
## Operations

```python
# get Domain entries registered with current Account
domains = puck.getDomains()

# get master ip address for specific domain
ip = puck.get_IP("mydomain.com")

# set ip address for single domain
puck.set_IP("ipv4.mydomain.com", "127.0.0.1")

# set same IP address for all domains
puck.setAllIP("::1")
```

## Logout
```python
puck.logout()
```

## Exceptions

| Exception | Explanation | Solution |
| :-: | :-: | :-: |
| NotLoggedIn | The instance isn't logged in | use login methode |
| LoginFailed | You provided wrong user credentials or network error | remember correct pwd or fix network |

