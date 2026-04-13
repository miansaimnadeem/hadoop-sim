import requests
import time
import socket
from collections import Counter

WORKERS = [
    "http://172.20.0.11:5000", # worker1
    "http://172.20.0.12:5000", # worker2
    "http://172.20.0.13:5000", # worker3
]

def split_file(path, n=3):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    chunk_size = len(lines) // n
    chunks = []
    for i in range(n):
        start = i * chunk_size
        end = (i+1) * chunk_size if i < n-1 else len(lines)
        chunks.append("".join(lines[start:end]))
    return chunks

print("=== MASTER NODE STARTING ===")
print(f"Master IP: {socket.gethostbyname(socket.gethostname())}")
time.sleep(8) # wait for workers to boot

# DATA CHUNKING
chunks = split_file('/app/dataset/big.txt', len(WORKERS))

# MAP PHASE
map_results = []
for i, worker_url in enumerate(WORKERS):
    try:
        print(f"[MAP] Sending chunk {i+1} to {worker_url}...")
        res = requests.post(f"{worker_url}/process", json={'chunk': chunks[i]}, timeout=15)
        data = res.json()
        print(f"[MAP] Got result from {data['worker_name']} ({data['worker_ip']})")
        map_results.append(data)
    except Exception as e:
        # ADVANCED: Node failure simulation
        print(f"[ERROR] {worker_url} FAILED! Reassigning to next worker...")
        backup_worker = WORKERS[(i+1) % len(WORKERS)]
        res = requests.post(f"{backup_worker}/process", json={'chunk': chunks[i]}, timeout=15)
        map_results.append(res.json())

# REDUCE PHASE
print("\n[REDUCE] Aggregating results...")
final_count = Counter()
for r in map_results:
    final_count.update(r['result'])

print("\n=== FINAL RESULT - Top 20 Words ===")
for word, count in final_count.most_common(20):
    print(f"{word}: {count}")

# save output
with open('/app/dataset/output.txt', 'w') as f:
    for w,c in final_count.most_common():
        f.write(f"{w},{c}\n")