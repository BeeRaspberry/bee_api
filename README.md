# bee_api
Repo is the Web API calls for processing data

## Work in Progress

## Setup
Notes for myself, as I forget everything.

In order to get `flask db migrate` to work, add the following to `env.py` residing in the `migrations` folder.

```python
from bee_api import models          # This line
config.set_main_option('sqlalchemy.url',
                       current_app.config.get('SQLALCHEMY_DATABASE_URI'))
target_metadata = models.Base.metadata # And this line
```
