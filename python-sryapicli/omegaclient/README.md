# omega-Client


## Install

``` 
git clone https://github.com/Dataman-Cloud/omega-client.git
   
    
cd omega-client/python-omegaclient/ 
   
    
pip3 install -r requirements.txt
    
    
python3 setup.py install
```   
    
## Use

```
>> from omegaclient import OmegaClient
>> client = OmegaClient(server_url, email, password)
>> client.get_clusters()
>> ...
```
## APIS

### Auth

#### get_token
```
Fetch user token
```
```
arguments: email - user email
           passed - user passed
           
returns: Dicitonary contains token
```

### User
```
Retrieve user information
```
```
arguments: None

returns: Dictionary contains user information
```

### Cluster

#### get_clusters

 ```
  List all clusters

  arguments: None

  returns: clusters list
```
#### get_cluster

```
  List single cluster's information

  arguments: cluster_id

  returns: cluster dictionary
```
#### delete_cluster

```
  Delete cluster

  arguments: cluster_id

  returns: None

```
#### create_cluster

```
  Create new cluster.

  arguments: name: cluster name - string
             cluster_type: cluster type - 1_master or 3_masters or 5_masters
             group_id: - int 

  returns: None

```

#### update_cluster
```
  Updated cluster information. currently only supported modifing the cluster name.
  
  arguments: cluster_id - 1000
             kwargs     - { "name": "new_cluster_name" }
  
  returns: { "code": 0 }
  
  
```

#### get_node_identifier

```
  Generated new node identifier. this identifier will be used for add new node.

  arguments: cluster_id

  returns: { "identifier": "string" }
  
```

#### get_cluster_node

```
  List node information

  arguments:
           cluster_id
           node_id

  returns: dictionary contans node information
  
    
  {
        "cluster": {
            "id": 0,
            "name": "string",
            "cluster_type": "string"
        },
        "id": "string",
        "name": "string",
        "status": "string",
        "created_at": "string",
        "ip": "string",
        "services": [
            {
            "name": "string",
            "status": "string"
        }
        ]
}
```

#### update_cluster_node

```
  Updated node information

  arguments:
           cluster_id
           node_id
           kwargs

  returns: 
          {
            "code": 0
          }
 
  status: 200
          401
```

#### get_node_metrics

```
  Retrive node metrics

  arguments:
            cluster_id
            node_id

  returns: metrics list
```

#### update_node_service

```
  Reset or restart service on node

  arguments:
           cluster_id
           node_id
           service_name
           kwargs

  returns: { "code": 0 }
```

#### create_node

```
  Add new node for cluster identified by `cluster_id`
  
  arguments: `cluster_id` `kwargs`

  returns: { "code": 0 }
```

#### delete_nodes

```
  Delete single node or multiple nodes

  arguments: `cluster_id` `args`

  returns: { "code": 0 }
```
            
### App

#### get_cluster_apps
```
List all apps in cluster
```
```
arguments: cluster_id

returns: apps list
```

#### create_cluster_apps
```
Created app in cluster
```
```
arguments: cluster_id - 100
           kwargs: - json object contains all parameters for app creation

returns: app id 
```

#### get_cluster_app
```
Show app information
```
```
arguments: cluster_id - 100
           app_id     - 699
          
returns: Dictionary contains app information
```

#### delete_cluster_app
```
Delete app
```
```
arguments: cluster_id - 100
           app_id     - 689
           
returns: None
```
#### get_user_apps
```
List all apps belong to a user
```
```
arguments: None

returns: List contains all apps
```

#### get_user_apps_status
```
List all app's status
```
```
arguments: None

return: List contains all app status
```
#### get_app_versions
```
List all history versions for app
```
```
arguments: cluster_id - 100
           app_id     - 101
           
returns: Dictionary contains all versions
```
#### delete_app_version
```
Delete app version
```
```
arguments: cluster_id - 100
           app_id     - 899
           version_id - 12
          
returns: None
```

#### update_cluster_app
```
Updated app configuration
```
```
arguments: cluster_id - 100
           app_id     - 688
           kwargs     - json object contains all app configurations

returns: None
```
#### get_app_instances
```
List all app instances
```
```
arguments: cluster_id - 100
           app_id     - 999
           
returns: List contains all versions
```

#### get_app_events
```
List all app events
```
```
arguments: cluster_id - 100
           app_id     - 345
           
returns: List contains all events
```

### Project

#### get_projects
```
List all projects(images)
```
```
arguments: None

returns: List contains all projects
```

#### create_project
```
Create new project
```
```
arguments: kwargs - json object contains all parameters for project creation

returns: dictionary contains new project information
```
#### build_project
```
Build image
```
```
arguments: project_id 
           uid
           image_name
returns: None
```
#### delete_project
```
Delete project
```
```
arguments: project_id - 109

returns: None
```

#### get_project
```
Show project information
```
```
arguments: project_id - 109

returns: Dictionary contains project information
```

#### update_project
```
Partially update project's information
```
```
arguments: project_id - 109
           kwargs - json object contains update information

retuns: None
```
#### get_project_builds
```
List all build versions
```
```
arguments: project_id

returns: List contains all builds
```

#### get_project_build_logs
```
List all build logs
```
```
arguments: project_id - 109
           build_num  - 88
           job_id     - 99
          
returns: List contains all build logs
```

#### get_project_build_stream
```
Retrieve build stream
```
```
arguments: project_id - 109
           build_num  - 99
           job_id     - 88
           
returns: build stream
```

### Logs

#### get_app_logs
```
List all app runtime logs
```
```
arguments: kwargs - json object contains the following keys:
                    userid    - user id
                    clusterid - cluster id
                    appname   - app name
                    start     - start time
                    end       - end time
                    from      - offset for page pagination
                    size      - log counts for page pagination
                    keyword   - keyword for search
                
returns: dictionary contains all app logs
```
`from` and `size` are used for page pagination

#### get_app_context
```
List all app context
```
```
arguments: charges - json object contains the following keys:
                     userid
                     clusterid
                     appname
                     timestamp
                     ipport
                     counter
                     source
returns: dictionary contains all app context
```

### Alert

#### get_tasks
```
Lists all the policies that the user created.
```
```
arguments: kwargs(optinal) - json object contains all query parameters:
		   
           keyword - search keyword
           sort_by - sort field
           order - ascending or descending
           per_page - entries per page 
           page - page offset
           
returns: List contains all user policies.
```
`per_page` and `page` are used for page pagination.

#### create_task
```
Created new policy.
```
```
arguments: json object contains all parameters for policy creation.

returns: Dictionary contans new policy information.
```

#### put_task
```
Updated policy information.
```
```
arguments: kwargs -json object

returns: None
```
#### patch_task
```
Updated policy status.
```
```
arguments:policy_id policy identifier 
          kwargs - json object

returns: None
```

#### get_task
```
List policy information.
```
```
arguments: policy_id - policy's identifier

returns: Dictionary contains policy information
```

#### delete_task
```
Delete policy
```
```
arguments: policy_id - policy's identifier

returns: None
```
#### get_events
```
List all alarm event's histories.
```
```
arguments: kwargs(optinal) - json object contains all query parameters:
		   
           keyword - search keyword
           sort_by - sort field
           order - ascending or descending
           per_page - entries per page 
           page - page offset
           
returns: List contains all alarm events.
```
`per_page` and `page` are used for page pagination.

### Metrics

#### get_app_history_metrics

```
arguments: cluster_id
           app_alias
           starttime (optional) - default one hour ahead of the current time in nanosecond
           endtime (optional) - default current time in nanosecond

returns: Dictionary contains metrics information.
```

#### get_app_requests
```
arguments: cluster_id
           app_alias
           starttime  - start time in nanosecond
           endtime - end time in nanosecond

returns: Dictionary contains metrics information.
```
#### get_app_live_metrics
```
arguments: cluster_id
           app_alias

returns: Dictionary contains metrics information.
```

#### get_cluster_resource_metrics
```
arguments: cluster_id

returns: Dictionary contains cluster metrics information.
```
