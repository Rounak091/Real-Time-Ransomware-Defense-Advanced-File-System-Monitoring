# Optimization Plan for Flask App (dashboard/app.py)

## Goal
Reduce CPU usage below 20% and memory usage below 30% when running the app.

## Information Gathered
- Flask app runs with debug=True, which increases resource usage.
- Background threads: monitoring_thread (file monitoring) and metrics_thread (collecting CPU/memory every 5s).
- Data structures: alerts list (keeps 50), performance_data (keeps 100 points).
- psutil.cpu_percent(interval=1) blocks for 1 second.
- Watchdog Observer monitors files recursively, potentially CPU-intensive.
- PerformanceOptimizer exists but not integrated.

## Plan
1. Integrate PerformanceOptimizer into app.py for automatic optimizations.
2. Disable debug mode (set debug=False).
3. Increase background metrics collection interval from 5s to 15s.
4. Reduce data retention: alerts to 20, performance_data to 50.
5. Optimize psutil calls: use interval=0.1 instead of 1.
6. Add CPU/memory thresholds and auto-optimization in background threads.
7. Limit file monitoring scope if possible.

## Dependent Files
- dashboard/app.py (main edits)
- monitor/performance_optimizer.py (already exists, integrate)

## Followup Steps
- Test the app after changes.
- Monitor CPU/memory usage.
- If needed, further reduce monitoring frequency or disable non-essential features.
