# System Metrics Dashboard

A real-time system metrics monitor built with **Flask**, **psutil**, and **Docker**. Displays CPU, memory, and disk usage in a clean web dashboard. Automatically built and containerized via **GitHub Actions** CI/CD.

## Features

- 📊 **Real-time metrics**: CPU usage, memory, disk space (refreshes every 2 seconds)
- 🎨 **Clean web UI**: Responsive dashboard with progress bars and color-coded warnings
- 🐳 **Docker containerized**: Run anywhere with `docker run`
- ⚙️ **GitHub Actions CI/CD**: Auto-builds and pushes Docker image to GitHub Container Registry on every commit
- 🏥 **Health checks**: Built-in container health monitoring
- 🔄 **JSON API**: RESTful `/api/metrics` endpoint for programmatic access

## Quick Start

### Local Development

```bash
# Clone the repo
git clone https://github.com/yourusername/metrics-dashboard
cd metrics-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

### Docker (Local)

```bash
docker build -t metrics-dashboard .
docker run -p 5000:5000 metrics-dashboard
```

### Docker (From Registry)

```bash
docker run -p 5000:5000 ghcr.io/yourusername/metrics-dashboard:latest
```

## Project Structure