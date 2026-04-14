# hadoop-sim
# Hadoop-like Distributed System Simulation using Docker

> Big Data Analytics | Simulating MapReduce with IP-based Docker Containers & Vibe Coding

This project simulates a real Hadoop cluster on a single laptop using Docker. It demonstrates the core concepts of **distributed computing, data chunking, MapReduce, and fault tolerance** without needing multiple physical machines.

### ✨ Live Demo Features
*   **1 Master + 3 Workers**, each with its own static IP address
*   **Map Phase:** Parallel word count on data chunks
*   **Reduce Phase:** Master aggregates results
*   **Advanced:** Automatic task reassignment on node failure

---

### 1. System Architecture

The system uses a custom Docker bridge network to mimic a real data center LAN.

```
[Your Laptop]
    |
    +-- [hadoop_net: 172.20.0.0/16]
            |
            +-- Master (172.20.0.2) -> Splits data, Sends tasks, Reduces results
            |
            +-- Worker1 (172.20.0.11) -> Map Task 1
            +-- Worker2 (172.20.0.12) -> Map Task 2
            +-- Worker3 (172.20.0.13) -> Map Task 3
```

**Communication:** Master talks to workers via HTTP REST API over their IPs (`http://172.20.0.11:5000/process`)

### 2. Tech Stack
*   **Containerization:** Docker & Docker Compose
*   **Backend:** Python 3.9, Flask (Worker API), Requests (Master Client)
*   **Development:** VS Code
*   **Methodology:** AI-Assisted Vibe Coding

### 3. Project Structure
```
hadoop-sim/
├── docker-compose.yml   # Defines 4 containers with static IPs
├── Dockerfile           # Python environment for all nodes
├── requirements.txt     # flask, requests
├── dataset/
│   └── big.txt          # Input dataset (download separately)
│   └── output.txt       # Final result (auto-generated)
├── master/
│   └── master.py        # Coordinator: splits, maps, reduces
└── worker/
    └── worker.py        # Worker: processes chunk
```

### 4. Getting Started

#### Prerequisites
1.  Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2.  Install [VS Code](https://code.visualstudio.com/)
3.  Verify installation: `docker --version`

#### Setup

    Download the dataset into the `dataset` folder:
    ```bash
    curl -o dataset/big.txt https://norvig.com/big.txt
    ```

### 5. How to Run

**This is the ONLY command you need.** Do NOT run `python master.py`.

```bash
docker compose up --build
```
> Note: If you have an older Docker version, use `docker-compose up --build`

**What happens:**
1. Docker builds 4 containers (1 master, 3 workers)
2. Master waits 8 seconds for workers to boot
3. Master splits `big.txt` into 3 chunks
4. Master sends each chunk to a worker via its IP (Map Phase)
5. Workers return word counts
6. Master aggregates and prints the Top 20 words (Reduce Phase)

**Expected Output:**
```
master   | === MASTER NODE STARTING ===
master   | [MAP] Got result from worker1 (172.20.0.11)
master   | [MAP] Got result from worker2 (172.20.0.12)
master   | [MAP] Got result from worker3 (172.20.0.13)
master   | === FINAL RESULT - Top 20 Words ===
master   | the: 80030
master   | of: 40024
```

The full result is saved in `dataset/output.txt`

**To stop:**
```bash
docker compose down
```

### 6. Testing Fault Tolerance (Advanced Feature)
While the cluster is running, open a NEW terminal and stop a worker:
```bash
docker stop worker2
```
Watch the master terminal. It will automatically detect the failure and reassign the task:
```
[ERROR] http://172.20.0.12:5000 FAILED! Reassigning to next worker...
```

### 7. Vibe Coding - Prompt Engineering Log

This project was built using iterative AI prompts, not traditional coding.

| Prompt Goal | Key Learning |
| :--- | :--- |
| Create static IP network in Docker | Learned `ipam` config for stable cluster |
| Build Flask worker for Map | Handled punctuation and encoding issues |
| Fix ConnectionRefusedError | Added `time.sleep()` for container startup race |
| Implement Reduce | Used `collections.Counter` for efficient aggregation |
| Simulate node failure | Implemented try/except reassignment logic |

Full prompt log is available in `/REPORT.pdf`

### 8. Debugging Highlights
*   **Issue:** Workers not ready when master sent data. **Fix:** Added startup delay.
*   **Issue:** `FileNotFoundError` for dataset. **Fix:** Correct Docker volume mount `./dataset:/app/dataset`.
*   **Issue:** VS Code yellow line under `flask`. **Fix:** Flask is installed *inside* Docker, not on host. This is normal.

### 9. Assignment Learning Outcomes
- [x] Understand distributed computing concepts
- [x] Implement MapReduce-like processing
- [x] Learn container-based simulation of clusters
- [x] Practice AI-assisted development (vibe coding)

---
**Author:** M. Saim | **Course:** Big Data Analytics
