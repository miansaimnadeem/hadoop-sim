from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    chunk = request.json['chunk']
    # MAP PHASE: simple word count
    words = chunk.lower().split()
    counts = {}
    for w in words:
        clean_w = w.strip('.,!?;:"()[]')
        if clean_w:
            counts[clean_w] = counts.get(clean_w, 0) + 1
    
    ip = socket.gethostbyname(socket.gethostname())
    return jsonify({
        'worker_ip': ip,
        'worker_name': socket.gethostname(),
        'result': counts
    })

@app.route('/')
def health():
    return "Worker OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)