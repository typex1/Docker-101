Here’s how you can **connect a Flask frontend container to a Redis storage container using only traditional Docker commands** (no Docker Compose). This approach is great for learning how containers communicate on the same network.

---

### **Project Structure**
```
flask_redis_manual/
├── app.py            # Flask application
├── requirements.txt  # Python dependencies
└── Dockerfile        # Dockerfile for Flask app
```

---

### **1. app.py**
```python
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Connect to Redis (use the container name 'redis' as the host)
redis_client = redis.Redis(host='redis', port=6379, db=0)

@app.route('/set', methods=['POST'])
def set_value():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    if not key or not value:
        return jsonify({'error': 'Key and value are required'}), 400
    redis_client.set(key, value)
    return jsonify({'message': f'Set {key} = {value}'}), 201

@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    value = redis_client.get(key)
    if value is None:
        return jsonify({'error': 'Key not found'}), 404
    return jsonify({'key': key, 'value': value.decode('utf-8')}), 200

@app.route('/')
def home():
    return "Flask + Redis Manual Docker Demo", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

### **2. requirements.txt**
```
flask==3.0.0
redis==5.0.1
```

---

### **3. Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

### **Step-by-Step: Running the Containers Manually**

#### **1. Create a Docker Network**
Containers need to be on the same network to communicate.
```bash
docker network create flask-redis-net
```

#### **2. Run the Redis Container**
```bash
docker run --name redis --network flask-redis-net -d redis:alpine
```
- `--name redis`: Names the container `redis` (used as the host in `app.py`).
- `--network flask-redis-net`: Attaches it to the custom network.

#### **3. Build the Flask Image**
```bash
docker build -t flask-app .
```

#### **4. Run the Flask Container**
```bash
docker run --name flask-app --network flask-redis-net -p 5000:5000 -d flask-app
```
- `--name flask-app`: Names the container.
- `--network flask-redis-net`: Attaches it to the same network as Redis.
- `-p 5000:5000`: Maps port 5000 on your machine to port 5000 in the container.

---

### **Testing the Setup**
- **Set a value**:
  ```bash
  curl -X POST http://localhost:5000/set -H "Content-Type: application/json" -d '{"key": "foo", "value": "bar"}'
  ```
- **Get a value**:
  ```bash
  curl http://localhost:5000/get/foo
  ```
  You should see:
  ```json
  {"key": "foo", "value": "bar"}
  ```

---

### **What This Demonstrates**
- **Manual Networking**: You create and manage the network yourself.
- **Container Communication**: The Flask app connects to Redis using the container name (`redis`) as the host.
- **Isolation**: Each container runs independently but can communicate over the shared network.
- **No Compose**: Everything is done with `docker build`, `docker run`, and `docker network`.

---

### **Cleanup**
To stop and remove the containers and network:
```bash
docker stop flask-app redis
docker rm flask-app redis
docker network rm flask-redis-net
```

---

This approach gives you full control and a deeper understanding of how Docker networking and container communication work under the hood.
