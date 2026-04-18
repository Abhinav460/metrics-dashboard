#!/usr/bin/env python3
"""
Real-time system metrics dashboard.
Displays CPU, memory, and disk usage in the browser.
"""

from flask import Flask, render_template, jsonify
import psutil
import json

app = Flask(__name__)


def get_metrics():
    """Collect current system metrics."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        'cpu': {
            'percent': cpu_percent,
            'count': psutil.cpu_count(logical=True),
            'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
        },
        'memory': {
            'percent': memory.percent,
            'used_gb': round(memory.used / (1024**3), 2),
            'total_gb': round(memory.total / (1024**3), 2),
        },
        'disk': {
            'percent': disk.percent,
            'used_gb': round(disk.used / (1024**3), 2),
            'total_gb': round(disk.total / (1024**3), 2),
        }
    }


@app.route('/')
def index():
    """Serve the main dashboard page."""
    return render_template('index.html')


@app.route('/api/metrics')
def metrics():
    """JSON endpoint for metrics (used by the dashboard)."""
    return jsonify(get_metrics())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)