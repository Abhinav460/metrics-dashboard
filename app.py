#!/usr/bin/env python3
"""
Real-time system metrics dashboard.
Displays CPU, memory, and disk usage in the browser.
"""

import threading
from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

# Sample CPU in a background thread so /api/metrics never blocks for 1s.
# psutil.cpu_percent(interval=None) returns 0.0 on the very first call;
# the thread keeps it warm by measuring continuously with interval=1.
_cpu_percent = 0.0
_cpu_lock = threading.Lock()


def _cpu_sampler():
    global _cpu_percent
    psutil.cpu_percent(interval=None)  # discard the first 0.0 reading
    while True:
        val = psutil.cpu_percent(interval=1)
        with _cpu_lock:
            _cpu_percent = val


threading.Thread(target=_cpu_sampler, daemon=True).start()


def get_metrics():
    """Collect current system metrics."""
    with _cpu_lock:
        cpu_percent = _cpu_percent

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    cpu_freq = psutil.cpu_freq()

    # Memory: psutil percent = (total - available) / total * 100.
    # memory.used only includes active+wired on macOS, so it doesn't match
    # percent. Use (total - available) so used_gb and percent are consistent.
    mem_used = memory.total - memory.available

    # Disk (macOS APFS): disk.used is the Data volume only; disk.total is the
    # full container. disk.percent = used/(used+free), where used+free << total
    # because System/Recovery/VM volumes consume the rest. Use (total - free)
    # as "used" so that used + free = total and percent is self-consistent.
    disk_used = disk.total - disk.free

    return {
        'cpu': {
            'percent': cpu_percent,
            'count': psutil.cpu_count(logical=True),
            # cpu_freq() returns None on Apple Silicon and some VMs
            'frequency': round(cpu_freq.current) if cpu_freq else None,
        },
        'memory': {
            'percent': round(mem_used / memory.total * 100, 1),
            'used_gb': round(mem_used / (1024 ** 3), 2),
            'total_gb': round(memory.total / (1024 ** 3), 2),
            'free_gb': round(memory.available / (1024 ** 3), 2),
        },
        'disk': {
            'percent': round(disk_used / disk.total * 100, 1),
            'used_gb': round(disk_used / (1024 ** 3), 2),
            'total_gb': round(disk.total / (1024 ** 3), 2),
            'free_gb': round(disk.free / (1024 ** 3), 2),
        },
    }


@app.route('/')
def index():
    """Serve the main dashboard page."""
    return render_template('index.html')


@app.route('/api/metrics')
def metrics():
    """JSON endpoint for live metrics."""
    return jsonify(get_metrics())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
