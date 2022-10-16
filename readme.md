
- [Task Manager Project](#task-manager-project)
  - [Endpoints](#endpoints)
      - [Create task](#create-task)
      - [Get all project tasks](#get-all-project-tasks)
      - [Get all task of a project assignee](#get-all-task-of-a-project-assignee)
      - [Update a task (assign it to another)](#update-a-task-assign-it-to-another)
      - [Sign up developer and manager](#sign-up-developer-and-manager)
  - [Running and test](#running-and-test)
    - [Build](#build)
    - [Running Tests](#running-tests)
    - [Running Dev](#running-dev)
    - [Creating super user for django admin](#creating-super-user-for-django-admin)
    - [Running In Production](#running-in-production)
    - [Scale Backend Service in production](#scale-backend-service-in-production)

# Task Manager Project
This is freshteam task management project.
The project has been developed by Django.

---
## Endpoints
#### Create task
```
method: POST
content-type: application/json
url: task-manager/api/v1/projects/<int:project_id>/tasks/
body: 
{
    "title": str,
    "description": str,
    "is_done": boolean,
    "assignee": [list of assignees id]
}
```

#### Get all project tasks
```
method: GET
url: task-manager/api/v1/projects/<int:project_id>/tasks
```

#### Get all task of a project assignee
```
method: GET
url: task-manager/api/v1/projects/<int:project_id>/assignee/<int:assignee_id>/tasks
```

#### Update a task (assign it to another)
```
method: PUT
content-type: application/json
url: task-manager/api/v1/projects/<int:project_id>/tasks/<int:pk>/
body: 
{
    "title": str,
    "description": str,
    "is_done": boolean,
    "assignee": [list of assignees id]
}

```

#### Sign up developer and manager
```
method: POST
content-type: application/json
url: task-manager/api/v1/projects/signup/
body: 
{
    "username":string
    "password":string
    "user_role": "developer" | "manager"
}
```
---
## Running and test
To run the below steps you need to have `docker` installed.

### Build
```
make build
```

### Running Tests
```
make test
```

### Running Dev
```
make run-dev
```

### Creating super user for django admin
```
make createsuperuser
```

### Running In Production
```
make run-prod
```

### Scale Backend Service in production
You can replace your desired number of replicas.
> **NOTE:**  You can scale the backend just after rining the project in production mode  with `"make run-prod"` command.
```
make scale-service replica-num=[number of service replicas]

ex:
make scale-service replica-num=5
```
