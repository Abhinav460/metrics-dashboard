# System Metrics Dashboard

A real-time system metrics monitor built with **Flask**, **psutil**, and **Docker**. Streams live CPU, memory, and disk usage to a browser dashboard that refreshes every 2 seconds.

---

## Overview

A background thread continuously samples `cpu_percent` so the API endpoint never blocks. Each request to `/api/metrics` returns a snapshot of CPU, memory, and disk in a normalized JSON shape — accounting for platform quirks like macOS APFS volume accounting and Apple Silicon's missing `cpu_freq`.

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Flask | 3.1.3 | Web framework, template rendering |
| psutil | 7.2.2 | Cross-platform system metrics |
| Werkzeug | 3.1.8 | WSGI utilities (Flask dependency) |
| Docker | — | Containerization |
| GitHub Actions | — | CI/CD — auto-build and push to GHCR |

---

## Features

- **Real-time metrics** — CPU usage (%), memory used/total/free (GB), disk used/total/free (GB); refreshes every 2 seconds
- **Non-blocking CPU sampling** — a daemon thread warms `psutil.cpu_percent` continuously so `/api/metrics` returns immediately without a 1-second measurement delay
- **Platform-aware math** — memory uses `total - available` (not `memory.used`) to stay consistent with psutil's `percent` on macOS; disk uses `total - free` to account for APFS multi-volume layouts
- **JSON API** — `/api/metrics` endpoint returns structured data for programmatic consumption or integration with external monitors
- **Docker containerized** — runs anywhere with a single `docker run` command
- **GitHub Actions CI/CD** — automatically builds and pushes a Docker image to GitHub Container Registry on every commit to `main`
- **Built-in health checks** — Docker `HEALTHCHECK` monitors the container

---

## Project Structure

```
metrics-dashboard/
├── app.py              # Flask app, background CPU sampler, metrics logic
├── templates/
│   └── index.html      # Dashboard frontend (auto-refreshes via JS)
├── Dockerfile
├── requirements.txt
└── READ.md
```

---

## Setup

### Local (no Docker)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/metrics-dashboard.git
cd metrics-dashboard

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
```

Open `http://localhost:5001` in your browser.

### Docker (local build)

```bash
docker build -t metrics-dashboard .
docker run -p 5001:5001 metrics-dashboard
```

### Docker (from GitHub Container Registry)

```bash
docker run -p 5001:5001 ghcr.io/your-username/metrics-dashboard:latest
```

---

## API Reference

### `GET /api/metrics`

Returns a JSON snapshot of current system metrics.

```json
{
  "cpu": {
    "percent": 14.3,
    "count": 8,
    "frequency": 2400
  },
  "memory": {
    "percent": 72.1,
    "used_gb": 11.54,
    "total_gb": 16.0,
    "free_gb": 4.46
  },
  "disk": {
    "percent": 58.2,
    "used_gb": 291.0,
    "total_gb": 500.0,
    "free_gb": 209.0
  }
}
```

`cpu.frequency` is `null` on Apple Silicon and some VMs where `psutil.cpu_freq()` returns `None`.

### `GET /`

Serves the live dashboard HTML page.

---

## CI/CD

GitHub Actions workflow (`.github/workflows/`) builds the Docker image and pushes it to GitHub Container Registry (`ghcr.io`) on every push to `main`. Pull the latest image with:

```bash
docker pull ghcr.io/your-username/metrics-dashboard:latest
```
