# Django user CRUD

Django app generic user CRUD based on MTV (Model-Template-View) architectural pattern with unit tests and using bootstrap version 4.0. Basic fluxogram with authentication, account creation, username edit and account exclusion.

Developed by: Remisson dos Santos Silva (www.github.com/remisson/)

# Requirements

> Python 3.12.3

> Django 6.1

> Bootstrap 4.0

> Mysql 8.4.11

# Build and Configuration

The first step is the docker configuration. We're gonna build the container to install app requirements and run the service. Assuming you're on the app base path (e.g /home/remisson/django--6-1-crud-user-bootstrap-mysql/), follow the instructions:

- Build all docker configurations by docker-compose:

1. Run the docker compose command

```
docker-compose up --build
```

2. Run kubernetes configuration

(Persistent option)
```
kubectl apply -f /k8s/userservice-api-deployment.yml
kubectl apply -f /k8s/userservice-mysql-pv.yml
kubectl apply -f /k8s/userservice-mysql-pvc.yml
kubectl apply -f /k8s/userservice-db-deployment-persistent.yml
kubectl apply -f /k8s/userservice-mysql-backup-cronjob.yml
kubectl apply -f /k8s/userservice-api-service.yml
```

(Non-persistent option)
```
kubectl apply -f /k8s/userservice-api-deployment.yml
kubectl apply -f /k8s/userservice-db-deployment.yml
kubectl apply -f /k8s/userservice-api-service.yml
```

- Build only the app container:

1. Build docker container app

```
docker build -t userservice .
```

2. Run container app

```
docker run -p 5000:5000 userservice
```

3. Run kubernetes configuration

```
kubectl apply -f /k8s/userservice.yml
```

- Configure the sensitive data files for application, docker and kubernetes, using swarm mode:

Docker compose

1. Run the follow commands, replacing the first params with the correct data:
```
echo "root_password" | docker secret create mysql_root_password -
echo "database_name" | docker secret create mysql_database -
echo "user" | docker secret create mysql_user -
echo "password" | docker secret create mysql_password -

docker secret ls
```

2. Run deployment commands:

```
docker swarm init
docker stack deploy -c docker-compose.yml userservice

docker service ls
docker secret ls
```

Kubernetes

1. Run the follow commands, replacing the first params with the correct data:
```
kubectl create secret generic mysql-secret \
  --from-literal=MYSQL_ROOT_PASSWORD=root_password \
  --from-literal=MYSQL_DATABASE=database_name \
  --from-literal=MYSQL_USER=user \
  --from-literal=MYSQL_PASSWORD=password

kubectl get secrets
kubectl describe secret mysql-secret
```
