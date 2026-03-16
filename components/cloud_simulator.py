import random
import time
import psutil
from datetime import datetime

class CloudSimulator:
    """Fake Cloud - lightweight & fast!"""
    
    def __init__(self):
        self.servers = 2
        self.base_capacity = 100  # 100 users per server
        self.current_load = 50
        self.cost_per_server = 50  # Rs per hour
        self.history = []
        self.logs = []
        
    def get_metrics(self):
        """Get current cloud status"""
        # Simulate traffic based on time
        hour = datetime.now().hour
        
        if 9 <= hour <= 18:  # Office hours
            base = 150
        elif 19 <= hour <= 23:  # Evening
            base = 200
        else:  # Night
            base = 80
            
        # Random variation
        spike = random.randint(-20, 30)
        self.current_load = max(10, base + spike)
        
        # Calculate
        capacity = self.servers * self.base_capacity
        utilization = (self.current_load / capacity) * 100 if capacity > 0 else 0
        
        # Real CPU/Memory (lightweight)
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory().percent
        except:
            cpu = random.randint(20, 60)
            memory = random.randint(30, 70)
        
        metrics = {
            'servers': self.servers,
            'current_load': self.current_load,
            'capacity': capacity,
            'utilization': round(utilization, 1),
            'cost_per_hour': self.servers * self.cost_per_server,
            'cpu_percent': round(cpu, 1),
            'memory_percent': round(memory, 1),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        
        # Save history
        self.history.append(metrics)
        if len(self.history) > 50:
            self.history = self.history[-50:]
            
        return metrics
    
    def scale_up(self):
        """Add server"""
        self.servers += 1
        msg = f"🚀 Scaled UP! Total servers: {self.servers}"
        self.logs.append(f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
        return msg
    
    def scale_down(self):
        """Remove server"""
        if self.servers > 1:
            self.servers -= 1
            msg = f"📉 Scaled DOWN! Total servers: {self.servers}"
            self.logs.append(f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
            return msg
        return "⚠️ Minimum 1 server required!"
    
    def get_logs(self):
        """Get recent logs"""
        return self.logs[-10:]
    
    def get_history(self):
        """Get metrics history for graphs"""
        return self.history
    
    def get_cost_insights(self):
        """💰 Smart cost analysis"""
        current_cost = self.servers * self.cost_per_server * 24
        
        optimal = max(1, (self.current_load // 80) + 1)
        
        savings = (self.servers - optimal) * self.cost_per_server * 24 if self.servers > optimal else 0
        
        return {
            'current_daily': current_cost,
            'optimal_servers': optimal,
            'potential_savings': int(savings),
            'efficiency': 'good' if self.servers == optimal else 'poor',
            'recommendation': f"Reduce to {optimal} servers" if self.servers > optimal else "Perfect!"
        }