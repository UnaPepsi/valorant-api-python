# Type-Safe Syncronous and Asyncronous Python wrapper for <a href='https://valorant-api.com/'>Valorant-API.com</a>

This library supports both **sync**, and **async** for its endpoints, is **type-checked** and supports **caching**

## Installation
```
pip install -U py-valorant
```

## Quick start
This API does not require any type of authentication key.

Each endpoint object is documented.

First, initialize a `ValorantAPI` or `ValorantAPIAsync` object
```py
#Sync
from py_valorant import ValorantAPI

api = ValorantAPI()
#Async
from py_valorant import ValorantAPIAsync

api = ValorantAPIAsync()
```

###### Parameters
- `language` **Optional[LANGUAGE]** - Defualts to `'en-US'`
  - The language of the supported returned strings (`localized` in the API).

Then you access any of the **attributes** inside that object. For this example, we'll use the `agent` attribute

### Fetch every agent
```py
#Sync
agents = api.agent.fetch_all()
#Async
agents = await api.agent.fetch_all()
```

###### Parameters
- `is_playable_character` **Optional[bool]** - Defualts to `False`
  - According to https://dash.valorant-api.com/endpoints/agents set this to `True` to remove possible duplicates
- `cache` **Optional[bool]** - Defualts to `False`
  - If `True` returns values saved in cache and if not found it fetches normally and saves to cache
  - If `False` removes the values previously cached by this method and its used parameters and fetches normally without caching
###### Returns
- `List[Agent]`

Now let's print to the console all the Agents' display name
```py
for agent in agents:
  print(str(agent)) # agent.display_name also works
```

### Convert a URL to bytes
```py
from py_valorant.utils import url_to_bytes

downloaded = url_to_bytes('https://exampleimage.com/image.png')
```
###### Parameters
- `url` **str**
  - The URL of the resource to convert
- `run_thread` **Optional[bool]** - Defualts to `False`
  - Whether to run the function in a new Thread
###### Returns
- `BytesIO`