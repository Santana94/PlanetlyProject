# Planetly Project

### Project development

- Basic Project Setup; 
Models creation; 
New migration file to add initial data: 30 minutes

- Basic serializers, viewsets and routers; 
correction to Usage model: 10 minutes
- New settings structure; basic JWT configuration: 20 minutes
- Testing; bug corrections; Swagger setup: 3 hours 
- Docker setup and final corrections: 1 hour

**Total development time: 5 hours**

How to use it
It is possible to use the web browser as an interface to interact with the application. It is possible to use Postman to make these actions as well.

## Setup
It is required to have make, docker and docker-compose installed for practical usage.
If you are using MacOS, it is recommended to use homebrew to make this process easier. 

## Requirements Installation

### Make Installation:

`sudo apt-get install make`

or

`brew install make`

### Docker Installation:

`sudo apt-get install docker.io`

or it's possible to install Docker Desktop for Mac

https://hub.docker.com/editions/community/docker-ce-desktop-mac

### Docker Compose Installation:

`sudo apt-get install docker-compose`

or

`brew install docker-compose`

### Run the project

To run the project use the following commands:

`make docker-migrate`

`make build`

`make up`

### Testing

It is possible to run the unittests for the project with the
following command:

`make test`

### Endpoints

The following endpoints are available to be accessed:

#### Usage API:

```buildoutcfg
http://0.0.0.0:8000/usage
http://0.0.0.0:8000/usage_types
```

#### Authentication:

```buildoutcfg
http://0.0.0.0:8000/api/token/
http://0.0.0.0:8000/api/token/refresh/
```

#### Documentation:

```buildoutcfg
http://0.0.0.0:8000/swagger
http://0.0.0.0:8000/redoc
```
