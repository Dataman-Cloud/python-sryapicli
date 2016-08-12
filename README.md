# shurenyun api command line tool

## Usage

1. To use this client tool, please login first with following command:
```
$python sryapi_cli.py login --host --email --password
```
arguments host, email and password must be specified.
password is prompted for credential when command is entered.

example:
```
$python sryapi_cli.py login --host="http://devforward.dataman-inc.net" --email cchen@dataman-inc.com --password
```

2. After login, user can get user info through command:
```
$python sryapi_cli.py user info
```

3. Meanwhile, user can logout through command:
```
$python sryapi_cli.py logout
```


## Commands
Following are all commands sryapi_cli supports currently:

### basic
```
$python sryapi-cli.py -h
```
```
usage: sryapi_cli [-h] [--version] COMMAND ...

shurenyun api client tool

positional arguments:
  COMMAND
    login        login with user email and password, api server is required
    logout       delete login user's token, return code 0 if success
    app          omega-app api command list
    log          search log command list
    user         get user information

optional arguments:
  -h, --help     show this help message and exit
  --version, -v  show program's version number and exit
```

### login

```
$python sryapi-cli.py login
```
```
usage: sryapi_cli login [-h] --host HOST --email EMAIL --password

optional arguments:
  -h, --help     show this help message and exit

authentication:
  --host HOST
  --email EMAIL
  --password
```
### user

```
$python sryapi-cli.py user -h
```
```
usage: sryapi_cli user [-h] ACTION ...

positional arguments:
  ACTION
    info      show current login user information

optional arguments:
  -h, --help  show this help message and exit
```

### app

```
$python sryapi-cli.py app -h
```
```
usage: sryapi_cli app [-h] ACTION ...

positional arguments:
  ACTION
    stop              stopa specified app
    start             starta specified app
    scale             scale instances for a specified app
    update_version    update app version
    get_cluster_apps  list all apps for specified cluster
    create            create app under specified cluster
    get               list specified app information under specified cluster
    delete            Delete specified app under specified cluster
    get_my_apps       list all apps belong to me.
    get_my_app_status
                      list all app's status
    get_app_version   list all history versions for a specific app
    delete_app_version
                      delete app version
    update_cluster_app
                      update app configuration
    get_app_instances
                      list all instances for a specific app
    get_app_events    list all events for a specific app
    get_app_nodes     list all nodes for a specific app
    get_cluster_ports
                      list the inner ports and outer ports for a specific
                      cluster
    get_app_scale_log
                      get the auto scale history when provided a strategy id
    get_my_scale_log  get all the auto scale history owned by this loggin user

optional arguments:
  -h, --help          show this help message and exit
```

### log

```
$python sryapi-cli.py log -h
```

```
usage: sryapi_cli log [-h] ACTION ...

positional arguments:
  ACTION
    search            search app controller log
    search_log_context
                      retrieve app log context

optional arguments:
  -h, --help          show this help message and exit
```
