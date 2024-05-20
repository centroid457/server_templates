# server_templates (v0.2.23)

## DESCRIPTION_SHORT
templates for servers

## DESCRIPTION_LONG
designed for keep all servers templates in one place


## Features
1. server:  
	- aiohttp (try not to use, as old)  
	- FastApi (preferred)  
2. client_requests item+stack  


********************************************************************************
## License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).


## Release history
See the [HISTORY.md](HISTORY.md) file for release history.


## Installation
```commandline
pip install server-templates
```


## Import
```python
from server_templates import *
```


********************************************************************************
## USAGE EXAMPLES
See tests and sourcecode for other examples.

------------------------------
### 1. example1.py
```python
import server_templates
import pathlib
import time


server = server_templates.ServerAiohttpBase()
server.start()
server.wait()
```

********************************************************************************
