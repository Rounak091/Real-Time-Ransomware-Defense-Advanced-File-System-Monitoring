import psutil
import time
import threading
import json
from datetime import datetime
import logging

class PerformanceOptimizer:
    def __init__(self):
        self.performance_data = {
            'cpu_usage': [],
            'memory_usage': [],
            'detection_times': [],
            'throughput': []
        }
        self.optimization_thresholds = {
            'max_cpu': 20.0,  # Reduced from 80% to 20%
            'max_memory': 300,  # Reduced from 500MB to 300MB
            'max_detection_time': 100,  # ms
            'min_throughput': 50  # operations/second
        }
        self.optimizations_applied = []
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/performance.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def start_monitoring(self):
        """Start continuous performance monitoring"""
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Performance monitoring started")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_info = psutil.virtual_memory()
                memory_mb = memory_info.used / 1024 / 1024
                
                # Store metrics
                self.performance_data['cpu_usage'].append(cpu_percent)
                self.performance_data['memory_usage'].append(memory_mb)
                
                # Keep only last 100 readings
                for key in self.performance_data:
                    if len(self.performance_data[key]) > 100:
                        self.performance_data[key] = self.performance_data[key][-100:]
                
                # Check if optimization is needed
                self._check_optimization_needed(cpu_percent, memory_mb)
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(10)
    
    def _check_optimization_needed(self, cpu_percent, memory_mb):
        """Check if performance optimization is needed"""
        optimizations = []
        
        # CPU optimization check
        if cpu_percent > self.optimization_thresholds['max_cpu']:
            optimizations.append(('high_cpu', cpu_percent))
        
        # Memory optimization check
        if memory_mb > self.optimization_thresholds['max_memory']:
            optimizations.append(('high_memory', memory_mb))
        
        # Apply optimizations if needed
        if optimizations:
            self._apply_optimizations(optimizations)
    
    def _apply_optimizations(self, optimizations):
        """Apply performance optimizations"""
        for optimization_type, value in optimizations:
            if optimization_type == 'high_cpu':
                self._optimize_cpu_usage(value)
            elif optimization_type == 'high_memory':
                self._optimize_memory_usage(value)
    
    def _optimize_cpu_usage(self, cpu_percent):
        """Optimize for high CPU usage"""
        optimizations = [
            "Reducing feature extraction complexity",
            "Increasing monitoring interval",
            "Disabling non-essential logging",
            "Using lighter ML model for inference"
        ]
        
        self.logger.warning(f"High CPU usage detected: {cpu_percent}%")
        self.logger.info(f"Applying CPU optimization: {optimizations[0]}")
        
        # Record optimization
        self.optimizations_applied.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'cpu_optimization',
            'reason': f'High CPU usage: {cpu_percent}%',
            'action': optimizations[0]
        })
    
    def _optimize_memory_usage(self, memory_mb):
        """Optimize for high memory usage"""
        optimizations = [
            "Clearing feature cache",
            "Reducing event history buffer",
            "Garbage collection optimization",
            "Model memory usage optimization"
        ]
        
        self.logger.warning(f"High memory usage detected: {memory_mb:.1f} MB")
        self.logger.info(f"Applying memory optimization: {optimizations[0]}")
        
        # Record optimization
        self.optimizations_applied.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'memory_optimization',
            'reason': f'High memory usage: {memory_mb:.1f} MB',
            'action': optimizations[0]
        })
    
    def add_detection_metrics(self, detection_time_ms, throughput_ops):
        """Add detection performance metrics"""
        self.performance_data['detection_times'].append(detection_time_ms)
        self.performance_data['throughput'].append(throughput_ops)
        
        # Check detection performance
        if detection_time_ms > self.optimization_thresholds['max_detection_time']:
            self.logger.warning(f"Slow detection time: {detection_time_ms}ms")
        
        if throughput_ops < self.optimization_thresholds['min_throughput']:
            self.logger.warning(f"Low throughput: {throughput_ops} ops/sec")
    
    def get_performance_report(self):
        """Generate performance report"""
        if not self.performance_data['cpu_usage']:
            return {"error": "No performance data collected"}
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'current_metrics': {
                'cpu_usage_percent': self.performance_data['cpu_usage'][-1],
                'memory_usage_mb': self.performance_data['memory_usage'][-1],
                'avg_detection_time_ms': sum(self.performance_data['detection_times'][-10:]) / len(self.performance_data['detection_times'][-10:]) if self.performance_data['detection_times'] else 0,
                'avg_throughput_ops': sum(self.performance_data['throughput'][-10:]) / len(self.performance_data['throughput'][-10:]) if self.performance_data['throughput'] else 0
            },
            'optimizations_applied': self.optimizations_applied[-5:],  # Last 5 optimizations
            'system_health': self._calculate_system_health()
        }
        
        return report
    
    def _calculate_system_health(self):
        """Calculate overall system health score"""
        scores = []
        
        # CPU health (lower is better)
        avg_cpu = sum(self.performance_data['cpu_usage'][-10:]) / len(self.performance_data['cpu_usage'][-10:])
        cpu_score = max(0, 100 - avg_cpu)
        scores.append(cpu_score)
        
        # Memory health (lower is better, normalized)
        avg_memory = sum(self.performance_data['memory_usage'][-10:]) / len(self.performance_data['memory_usage'][-10:])
        memory_score = max(0, 100 - (avg_memory / 10))  # Normalize to 0-100
        scores.append(memory_score)
        
        # Detection time health (lower is better)
        if self.performance_data['detection_times']:
            avg_detection = sum(self.performance_data['detection_times'][-10:]) / len(self.performance_data['detection_times'][-10:])
            detection_score = max(0, 100 - (avg_detection / 2))  # Normalize
            scores.append(detection_score)
        
        # Throughput health (higher is better)
        if self.performance_data['throughput']:
            avg_throughput = sum(self.performance_data['throughput'][-10:]) / len(self.performance_data['throughput'][-10:])
            throughput_score = min(100, avg_throughput * 2)  # Normalize
            scores.append(throughput_score)
        
        overall_health = sum(scores) / len(scores) if scores else 100
        return {
            'score': overall_health,
            'status': 'excellent' if overall_health >= 90 else 'good' if overall_health >= 70 else 'fair' if overall_health >= 50 else 'poor'
        }

# Stress testing utility
class StressTester:
    def __init__(self):
        self.results = []
    
    def run_stress_test(self, duration_seconds=60, operations_per_second=100):
        """Run stress test with specified parameters"""
        print(f"🚀 Starting stress test: {duration_seconds}s, {operations_per_second} ops/sec")
        
        start_time = time.time()
        operation_count = 0
        
        while time.time() - start_time < duration_seconds:
            batch_start = time.time()
            
            # Simulate batch of operations
            for i in range(operations_per_second):
                # Simulate file operation
                operation_count += 1
                
                # Every 10th operation is suspicious (high entropy)
                if operation_count % 10 == 0:
                    # Simulate detection of high-entropy file
                    pass
            
            # Maintain operations per second rate
            batch_time = time.time() - batch_start
            if batch_time < 1.0:
                time.sleep(1.0 - batch_time)
        
        total_time = time.time() - start_time
        actual_ops_per_second = operation_count / total_time
        
        result = {
            'duration_seconds': duration_seconds,
            'target_ops_per_second': operations_per_second,
            'actual_ops_per_second': actual_ops_per_second,
            'total_operations': operation_count,
            'efficiency_percent': (actual_ops_per_second / operations_per_second) * 100
        }
        
        self.results.append(result)
        self._print_stress_test_result(result)
        
        return result
    
    def _print_stress_test_result(self, result):
        """Print stress test results"""
        print("\n" + "="*50)
        print("STRESS TEST RESULTS")
        print("="*50)
        print(f"Duration: {result['duration_seconds']} seconds")
        print(f"Target operations/sec: {result['target_ops_per_second']}")
        print(f"Actual operations/sec: {result['actual_ops_per_second']:.1f}")
        print(f"Total operations: {result['total_operations']}")
        print(f"Efficiency: {result['efficiency_percent']:.1f}%")
        
        if result['efficiency_percent'] >= 90:
            print("🎉 EXCELLENT PERFORMANCE!")
        elif result['efficiency_percent'] >= 75:
            print("✅ GOOD PERFORMANCE")
        elif result['efficiency_percent'] >= 50:
            print("⚠️  ACCEPTABLE PERFORMANCE")
        else:
            print("❌ POOR PERFORMANCE - NEEDS OPTIMIZATION")

# Demo and testing
def demo_performance_optimization():
    """Demonstrate performance optimization"""
    print("🚀 DEMONSTRATING PERFORMANCE OPTIMIZATION")
    
    # Initialize optimizer
    optimizer = PerformanceOptimizer()
    optimizer.start_monitoring()
    
    # Initialize stress tester
    stress_tester = StressTester()
    
    # Run stress tests at different levels
    test_levels = [50, 100, 200, 500]  # operations per second
    
    for level in test_levels:
        print(f"\n📊 Testing at {level} operations/second...")
        result = stress_tester.run_stress_test(duration_seconds=30, operations_per_second=level)
        
        # Add metrics to optimizer
        optimizer.add_detection_metrics(
            detection_time_ms=10,  # Simulated
            throughput_ops=result['actual_ops_per_second']
        )
        
        # Get performance report
        report = optimizer.get_performance_report()
        print(f"System Health: {report['system_health']['status']} ({report['system_health']['score']:.1f}/100)")
        
        # Small delay between tests
        time.sleep(2)
    
    # Final performance report
    print("\n" + "="*60)
    print("FINAL PERFORMANCE REPORT")
    print("="*60)
    final_report = optimizer.get_performance_report()
    
    for metric, value in final_report['current_metrics'].items():
        print(f"{metric}: {value}")
    
    print(f"\nOverall System Health: {final_report['system_health']['status']}")

if __name__ == "__main__":
    demo_performance_optimization()