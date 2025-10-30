Here is the content converted into a clean, copy-paste-friendly Markdown document:

# Deploying a Three-Tier App on Kubernetes: A Simple Guide

## Introduction
Deploying a multi-tier application on Kubernetes is like building a house: you need a strong foundation (database), sturdy walls (backend), and a beautiful façade (frontend). This guide simplifies deploying a three-tier application on Kubernetes using YAML files and straightforward commands.

---

## Prerequisites
- A Kubernetes cluster (Minikube, Kind, or cloud providers like GKE, EKS, or AKS).
- `kubectl` configured to communicate with your cluster.
- Docker (or a container registry) with your application images (`frontend-image:latest` and `backend-image:latest`).

---

## 1. Database Deployment (MySQL)

### `mysql-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        ports:
        - containerPort: 3306
        envFrom:
          - secretRef:
              name: mysql-password
```

### Create a Kubernetes Secret for MySQL Password
```bash
kubectl create secret generic mysql-password --from-literal=MYSQL_ROOT_PASSWORD=<your_strong_password>
```

---

## 2. Backend Deployment

### `backend-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: backend-image:latest
        ports:
        - containerPort: 8080
```

---

## 3. Frontend Deployment

### `frontend-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: frontend-image:latest
        ports:
        - containerPort: 80
```

---

## 4. Services

### `services.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer

# Repeat for backend-service and mysql-service, adjusting ports accordingly.
```

---

## 5. Deployment and Verification

### Apply the Configurations
```bash
kubectl apply -f mysql-deployment.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f services.yaml
```

### Check Status
```bash
kubectl get deployments
kubectl get services
```

---

## 6. Testing
Access your application through the external IP of the `frontend-service`. Ensure all components communicate correctly.

---

## Conclusion
You’ve successfully deployed a multi-tier application on Kubernetes! Adjust configurations (service type, resource limits, persistent volumes) as needed for production.

**Note:** Replace placeholders like `<your_strong_password>` with actual values. Consider adding persistent storage for the database and robust error handling for production.

---
You can now copy and paste the YAML and command-line snippets directly from this Markdown document.
