# Django user CRUD

Django app generic user CRUD based on MTV (Model-Template-View) architectural pattern with unit tests and using bootstrap version 4.0. Basic fluxogram with authentication, account creation, username edit and account exclusion.

Developed by: Remisson dos Santos Silva (www.github.com/remisson/)

# Requirements

> Python 3.12.3

> Django 5.2.17

> Bootstrap 4.0

> Mysql 8.4.11

> Docker 29.7.2

> Kubernetes (Client Version: v1.36.3 | Kustomize Version: v5.8.1)

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

# 1. Start minikube with docker driver
minikube start --driver=docker
minikube status

# 2. Verify nodes
```
kubectl get nodes
```

# 3. Create the Mysql secrets file
```
kubectl create secret generic mysql-secret \
  --from-literal=MYSQL_ROOT_PASSWORD=root_password \
  --from-literal=MYSQL_DATABASE=database_name \
  --from-literal=MYSQL_USER=username \
  --from-literal=MYSQL_PASSWORD=user_password

kubectl get secrets
kubectl describe secret mysql-secret
```

# 4. Set minikube env
```
eval $(minikube docker-env)
```

# 5. Create Mysql imagem and apply manifests and check log
```
minikube image build -t userservice-mysql:8.4.11 .

kubectl apply -f k8s/userservice-mysql-pv.yml
kubectl apply -f k8s/userservice-mysql-pvc.yml
kubectl apply -f k8s/userservice-db-deployment-persistent.yml
kubectl apply -f k8s/userservice-mysql-service.yml

kubectl logs deployment/userservice-db-deployment
```

# 6. Build web image
```
minikube image build -t userservice-web:latest .
```

build with docker and load with minikube
```
docker build -t userservice-web:latest .
minikube image load userservice-web:latest
```

# 7. Apply web manifests
```
kubectl apply -f k8s/userservice-web-deployment.yml
kubectl apply -f k8s/userservice-web-service.yml
```

# 8. Check if everything works
```
kubectl get pods
kubectl get svc
```

if the container has been created by build docker and load with minikube
```
minikube service userservice-web-service
```

# 9. Discover the ip
```
minikube ip
```

# 10. Access the application
```
e.g http://192.168.49.2:32571/
```

# Logger

Application log
```
kubectl logs deployment/userservice-web
```

Docker log
```
docker logs userservice_container
```
