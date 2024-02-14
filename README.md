# server_templates (v0.1.15)

## DESCRIPTION_SHORT
templates for servers

## DESCRIPTION_LONG
designed for keep all servers templates in one place


## Features
1. aiohttp  


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
