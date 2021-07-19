# Usage
## Prerequisites
1. Install [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)
2. Install [poetry](https://python-poetry.org/docs/#installation)

## Run cookiecutter to initialize a new Python project
```
PS C:\Users\testuser\projects> cookiecutter https://github.com/s-raza/cookiecutter-poetry-vscode --directory standard
project_name [pythonproject]:
pyversion [3.9]:
authors [[]]:
black_target_versions [["py39"]]:

Installing poetry virtual env ...done
Poetry virtual env installed at: C:\Users\testuser\AppData\Local\pypoetry\Cache\virtualenvs\pythonproject-B9yC7h6M-py3.9
Initializing GIT repo ...done
Installing pre-commit ...done
Auto Updating pre-commit ...done
Adding project files to GIT repo ...done
Committing to GIT repo ...done
Updating vscode config with virtual env path ...done
```

# Cookiecutter Features

1. Intializes [Python](https://www.python.org
) virtual environment using [Poetry](https://python-poetry.org/). Poetry should be [installed](https://python-poetry.org/docs/#installation) and [configured](https://python-poetry.org/docs/configuration/) before running [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/).
2. Installs development modules within the Poetry virtual environment with basic configurations for - pytest, pytest-cov, ptpython, pre-commit, flake8, black, mypy and isort.
3. Initializes a local Github repository for the files and folders rendered by cookiecutter.
4. Installs pre-commit hooks in GIT for pre-commit, flake8, black, mypy and isort
5. Autoupdates all the defined hooks in GIT for pre-commit
6. Renders a basic vscode settings.json file with a dark theme.
7. Updates the vscode pythonPath setting with the virtual environment python path created using Poetry.
8. Performs an initial GIT commit of the rendered cookiecutter project, with pre-defined files to ignore in .gitignore.
# Python Features

Settings for your Python program can be defined in two locations - `.json` files in the `config` directory and its sub directories or the `.env` file. The `config` directory is rendered by cookiecutter in the main project directory by default.

Once the settings are defined in either of these locations, they can be accessed by importing the `config.py` module anywhere in your code.

The values of the configuration keys with the same name accross all the setting sources (`config` directory and `.env`) are collected under a common key name.

***Example Usage***

*Settings from `pythonproject/config/config.json`*
```
{
    "env_config_key": "default_",
    "emailer": {
        "send": true
    }
}
```

*Settings from `pythonproject/config/emailer/email_config.json`*
```
{
    "emailer": {
        "subject": "Subject",
        "body": "Body"
    }
}
```

*Settings from `.env`*
```
default_emailer = {"username": "Username", "password": "Password", "api_key": {"secret": "Secret", "key": "KEY"}}
```

*Using the config settings defined above in your program*
```
C:\Users\testuser\projects\pythonproject>ptpython
>>> import pythonproject.config as cfg
>>> import pprint as pp

>>> pp.pp(cfg.emailer)
{'send': True,
 'subject': 'Subject',
 'body': 'Body',
 'username': 'Username',
 'password': 'Password',
 'api_key': {'secret': 'Secret', 'key': 'KEY'}}

>>> cfg.emailer["api_key"]["secret"]
'Secret'

>>> cfg.emailer["api_key"]["key"]
'KEY'

>>> cfg.emailer['send'] is False
False
```

**Settings from json config file**

Files with `.json` extension in the `config` directory can be organized into sub directories having one or more `.json` files. As long as the file extension is `.json` and the contents of it follow standard json formatting, the settings will be accessible in your Python progam.

Each key from all the `.json` files found in the `config` folder and its sub-folders is added to the global namespace of the config.py module.
<br>

**Sensitive settings from .env files**

This is to be used to populate sensitive settings like passwords and API keys. The `.env` file is excluded by default from the GIT repository created during intialization of the cookiecutter project.

Settings in the `.env` file can be defined just like environment variables. However a prefix string should be attached to each setting entry, which should be defined in one of the `.json` files in the `config` directory with the `env_config_key`. A default `env_config_key` with the value `default_` is already defined in the `config/config.json` file that is rendered by cookiecutter. Settings that do not have this prefix in the `.env` file are ignored.

**Database settings**

1. *Connecting to a database server*

    If a key "active_database" is defined in either config/config.json or .env files (default key prefix is applied to settings from .env as explained above) the database key corresponding to the database settings is populated into a 'database' variable in the global namespace of config.py. If an "active_database" key is not defined, the 'database' variable will be initialized to None.

    *Example using **.env:***
    ```
    default_test_db = {"dialect": "mysql+mysqldb","user": "dbuser","password": "dbuserpass","host": "localhost","db_name": "dbname","db_port": null,"db_options": {"charset": "utf8mb4"},"sqlalchemy_options": {"pool_recycle": 3600}}

    default_active_database = "test_db"
    ```

    We have a setting `default_active_database` in the .env file which will be available as `active_database` in the global namespace of config.py. The value of the `active_database` variable will be "test_db"
    <br><br>
    There is also a setting `default_test_db` which will be available as `test_db` in the global name space of config.py. The value of the `test_db` variable will be the dictionary with the database settings assigned to the `default_test_db` in the .env file.
    <br><br>
    Effectively a `database` variable will be initialized in the global namespace of config.py, with the settings dictionary assigned to `default_test_db` in the .env file.
    <br><br>
    Addtionally a `conn_string` key will be constructed and added to the `database` variable.
    <br><br>
    Demo:
    ```
    PS C:\Users\testuser> cd .\projects\pythonproject\
    PS C:\Users\testuser\projects\pythonproject> poetry shell
    Spawning shell within C:\Users\testuser\AppData\Local\pypoetry\Cache\virtualenvs\pythonproject-B9yC7h6M-py3.9
    Microsoft Windows [Version 10.0.19042.1083]
    (c) Microsoft Corporation. All rights reserved.

    C:\Users\testuser\projects\pythonproject>ptpython
    >>> import pythonproject.config as cfg
    >>> import pprint as pp

    >>> pp.pp(cfg.database, indent=4)
    {   'dialect': 'mysql+mysqldb',
        'user': 'dbuser',
        'password': 'dbuserpass',
        'host': 'localhost',
        'db_name': 'dbname',
        'db_port': None,
        'db_options': {'charset': 'utf8mb4'},
        'sqlalchemy_options': {'pool_recycle': 3600},
        'conn_string': 'mysql+mysqldb://dbuser:dbuserpass@localhost/dbname?charset=utf8mb4&'}

    >>> cfg.database['conn_string']
    'mysql+mysqldb://dbuser:dbuserpass@localhost/dbname?charset=utf8mb4&'

    >>> cfg.active_database
    'test_db'

    >>> pp.pp(cfg.test_db, indent=4)
    {   'dialect': 'mysql+mysqldb',
        'user': 'dbuser',
        'password': 'dbuserpass',
        'host': 'localhost',
        'db_name': 'dbname',
        'db_port': None,
        'db_options': {'charset': 'utf8mb4'},
        'sqlalchemy_options': {'pool_recycle': 3600},
        'conn_string': 'mysql+mysqldb://dbuser:dbuserpass@localhost/dbname?charset=utf8mb4&'}
    ```

2. *Connecting to SQLITE*

    If the activated database setting has a 'sqlite' key, it's value is assigned as the file name for the SQLITE file in the connection string for it.

    *Cotents of `pythonproject/config/config.json`*
    ```
    {
        "env_config_key": "default_",
        "test_db": {"sqlite": "sqlite_file.db"}
    }
    ```

    *Cotents of `pythonproject/.env`*
    ```
    default_project_name = pythonproject

    default_test_db = {"dialect": "mysql+mysqldb","user": "dbuser","password": "dbuserpass","host": "localhost","db_name": "dbname","db_port": null,"db_options": {"charset": "utf8mb4"},"sqlalchemy_options": {"pool_recycle": 3600}}

    default_active_database = "test_db"
    ```

    *Usage*
    ```
    C:\Users\testuser\projects\pythonproject>ptpython
    >>> import pythonproject.config as cfg
    >>> import pprint as pp

    >>> pp.pp(cfg.database, indent=4)
    {   'sqlite': 'sqlite_file.db',
        'dialect': 'mysql+mysqldb',
        'user': 'dbuser',
        'password': 'dbuserpass',
        'host': 'localhost',
        'db_name': 'dbname',
        'db_port': None,
        'db_options': {'charset': 'utf8mb4'},
        'sqlalchemy_options': {'pool_recycle': 3600},
        'conn_string': 'sqlite:///sqlite_file.db'}

    >>> cfg.database["conn_string"]
    'sqlite:///sqlite_file.db'
    ```
