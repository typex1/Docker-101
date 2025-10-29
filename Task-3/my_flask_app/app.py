from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Connect to Redis
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
    return "Flask + Redis Docker Demo", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

