# System Metrics Dashboard

A real-time system metrics monitor built with **Flask** and **psutil**. Displays live CPU, memory, and disk usage in a browser dashboard that auto-refreshes every 2 seconds.

---

## Overview

A background thread continuously samples CPU usage so the API never blocks on a measurement delay. Each request to `/api/metrics` returns a normalized JSON snapshot of CPU, memory, and disk — with platform-aware math for macOS APFS volumes and Apple Silicon.

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Flask | 3.1.3 | Web framework, template rendering |
| psutil | 7.2.2 | Cross-platform system metrics collection |
| Werkzeug | 3.1.8 | WSGI utilities (Flask dependency) |

---

## Features

- **Real-time metrics** — CPU (%), memory and disk used/total/free in GB; refreshes every 2 seconds
- **Non-blocking CPU sampling** — daemon thread keeps `cpu_percent` warm so `/api/metrics` returns instantly without a 1-second stall
- **Platform-aware math** — memory uses `total - available` to stay consistent with psutil's `percent` on macOS; disk uses `total - free` to handle APFS multi-volume layouts correctly
- **JSON API** — `/api/metrics` endpoint for programmatic access or integration with other tools
- **Zero config** — no API keys, no database, no environment variables needed

---

## Project Structure

```
metrics-dashboard/
├── app.py              # Flask app, background CPU sampler, route handlers
├── templates/
│   └── index.html      # Dashboard frontend (auto-refreshes via JS)
├── requirements.txt
└── READ.md
```

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/Abhinav460/metrics-dashboard.git
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

---

## API Reference

### `GET /`

Serves the live dashboard page.

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
