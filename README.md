# Django user CRUD

Django app generic user CRUD based on MTV (Model-Template-View) architectural pattern with unit tests and using bootstrap version 4.0. Basic fluxogram with authentication, account creation, username edit and account exclusion.

Developed by: Remisson dos Santos Silva (www.github.com/remisson/)

# Requirements

> Python 3.12.3

> Django 5.2.17

> Bootstrap 4.0

> Mysql 8.4.11

# Build application with Docker Swarm

Assuming you're on the app base path (e.g /home/remisson/django-crud-user-bootstrap-mysql/), follow the instructions:

1. Initializing docker swarm:
```
docker swarm init
```

2. Set secret params:

```
echo "root_password" | docker secret create mysql_root_password -
echo "database_name" | docker secret create mysql_database -
echo "user" | docker secret create mysql_user -
echo "password" | docker secret create mysql_password -
```

3. Check the created secrets:
```
docker secret ls
```

4. Set up docker compose:
```
docker stack deploy -c docker-compose.yml userservice_stack
```

# Build application with Kubernetes

Assuming you're on the app base path (e.g /home/remisson/django-crud-user-bootstrap-mysql/), follow the instructions:

1. Start minikube and verify the status and test the connection
```
minikube start
minikube status

kubectl get nodes
```

2. Run the follow commands, replacing the first params with the correct data:
```
kubectl create secret generic mysql-secret \
  --from-literal=MYSQL_ROOT_PASSWORD=root_password \
  --from-literal=MYSQL_DATABASE=database_name \
  --from-literal=MYSQL_USER=user \
  --from-literal=MYSQL_PASSWORD=password

kubectl get secrets
kubectl describe secret mysql-secret
```

3. Build docker container
```
eval $(minikube docker-env)
docker build -t userservice:latest .
```

4. Apply manifests:
```
kubectl apply -f /k8s/userservice-mysql-pv.yml
kubectl apply -f /k8s/userservice-mysql-pvc.yml
kubectl apply -f /k8s/userservice-db-deployment-persistent.yml
kubectl apply -f /k8s/userservice-mysql-service.yml
kubectl apply -f /k8s/userservice-api-deployment.yml
kubectl apply -f /k8s/userservice-api-service.yml
kubectl apply -f /k8s/userservice-web-deployment.yml
kubectl apply -f /k8s/userservice-web-service.yml
```

5. Accessing the services:
```
minikube service userservice-web-service
minikube service userservice-api-service
```

# Logger

Run the follow command to check the application logging out:

```
docker logs userservice_container
```
