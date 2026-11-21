# Real-Time Operations Monitoring and Alerting (ZAPPTTO Delivery Service)

This project simulates real-time delivery operations metrics, exposes them via a Python Prometheus client, scrapes them with Prometheus, visualizes them with Grafana dashboards, and sets up automated alerting and a Jenkins CI/CD pipeline.

---

## 📁 Directory Structure

```text
delivery_monitoring/
├── delivery_metrics.py     # Python script to simulate real-time metrics (Port 8000)
├── prometheus.yml          # Prometheus scrape and alerting configuration
├── alert_rules.yml         # Prometheus alert rules for high pending orders & delivery times
├── alerts_rules.yml        # Alias for alert_rules.yml
├── Jenkinsfile             # Jenkins pipeline script for automation
├── Dockerfile              # Container definition for the Python metrics service
├── docker-compose.yml      # Multi-service stack (App, Prometheus, Grafana, Jenkins)
├── requirements.txt        # Python dependencies (prometheus_client)
└── README.md               # Complete setup and troubleshooting guide
```

---

## 🚀 Quick Start Guide

### Option A: Running with Docker Compose (All-in-One)

Ensure **Docker Desktop** is running, then run:

```bash
cd delivery_monitoring
docker compose up -d
```

This launches:
- **Delivery Metrics App:** `http://localhost:8000/metrics`
- **Prometheus UI:** `http://localhost:9090`
- **Grafana Dashboard:** `http://localhost:3000` (User: `admin`, Pass: `admin`)
- **Jenkins:** `http://localhost:8080`

To stop:
```bash
docker compose down
```

---

### Option B: Step-by-Step Setup

#### Step 1: Run the Python Metrics Simulator

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the delivery metrics server:
   ```bash
   python delivery_metrics.py
   ```
3. Test metrics endpoint in your browser or terminal:
   ```bash
   curl http://localhost:8000/metrics
   ```

#### Step 2: Run Prometheus

Run Prometheus in Docker pointing to the config files:

- **Windows / macOS (PowerShell):**
  ```powershell
  docker run -d --name prometheus -p 9090:9090 `
    -v ${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml `
    -v ${PWD}/alert_rules.yml:/etc/prometheus/alert_rules.yml `
    prom/prometheus
  ```

- **Linux:**
  ```bash
  docker run -d --name prometheus --network=host \
    -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
    -v $(pwd)/alert_rules.yml:/etc/prometheus/alert_rules.yml \
    prom/prometheus
  ```

Access Prometheus:
- **Web UI:** [http://localhost:9090](http://localhost:9090)
- **Targets Status:** [http://localhost:9090/targets](http://localhost:9090/targets)
- **Alerts Status:** [http://localhost:9090/alerts](http://localhost:9090/alerts)

> **Network Note for Prometheus Targets:**
> - In Docker on Windows/Mac, host services are reached via `host.docker.internal:8000`.
> - In Linux with `--network=host`, use `172.17.0.1:8000` or `localhost:8000`.

#### Step 3: Run Grafana

1. Start Grafana:
   ```bash
   docker run -d --name grafana -p 3000:3000 grafana/grafana
   ```
2. Open [http://localhost:3000](http://localhost:3000)
   - **Username:** `admin`
   - **Password:** `admin` (skip password change on first prompt)
3. Add Prometheus as Data Source:
   - Navigate to: **Connections** → **Data sources** → **Add data source** → **Prometheus**
   - **URL:** 
     - If Grafana is in Docker and Prometheus is on host port 9090: `http://host.docker.internal:9090` (Windows/Mac) or `http://172.17.0.1:9090` (Linux)
     - If using docker-compose: `http://prometheus:9090`
   - Click **Save & Test**
4. Create Dashboard Panels:
   - **Panel 1 - Total Deliveries:**
     - Query: `total_deliveries`
     - Visualization: Stat / Gauge / Time series
   - **Panel 2 - Pending Deliveries:**
     - Query: `pending_deliveries`
     - Visualization: Stat / Gauge
   - **Panel 3 - On-the-Way Deliveries:**
     - Query: `on_the_way_deliveries`
     - Visualization: Time series
   - **Panel 4 - Average Delivery Time:**
     - Query: `average_delivery_time_sum / average_delivery_time_count`
     - Visualization: Gauge / Stat (Threshold > 30s)

#### Step 4: Run Jenkins and Execute Pipeline

1. Start Jenkins:
   ```bash
   docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
   ```
2. Retrieve initial admin password:
   ```bash
   docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Open [http://localhost:8080](http://localhost:8080), enter password, install suggested plugins, and create admin user.
4. Create Pipeline Job:
   - Click **New Item** → Name it `Delivery-Monitoring-Pipeline` → Select **Pipeline** → Click **OK**.
   - Scroll to **Pipeline** section, choose **Pipeline script**.
   - Copy the content of `Jenkinsfile` into the script area.
   - Click **Save** and then **Build Now**.

---

## 🔔 Simulating and Verifying Alerts

To trigger the `HighPendingDeliveries` alert:

1. In `delivery_metrics.py`, change:
   ```python
   pending = random.randint(10, 20)
   ```
   to:
   ```python
   pending = random.randint(50, 100)  # Exceeds the > 10 alert threshold
   ```
2. Save and restart `delivery_metrics.py`.
3. Open Prometheus at [http://localhost:9090/alerts](http://localhost:9090/alerts):
   - Within 15 seconds, the `HighPendingDeliveries` state will change from **Inactive** → **Pending** → **Firing** (Red).

