import random

class MultiCloudManager:
    """AWS + Azure + GCP simulate karega!"""
    
    def __init__(self):
        self.providers = {
            'AWS': {'cost_factor': 1.0, 'speed': 'fast', 'color': '#FF9900'},
            'Azure': {'cost_factor': 0.9, 'speed': 'medium', 'color': '#0089D6'},
            'GCP': {'cost_factor': 0.85, 'speed': 'fast', 'color': '#4285F4'}
        }
        self.current_provider = 'AWS'
        self.savings_history = []
    
    def get_best_provider(self, load):
        """Load ke hisaab se best provider suggest karega"""
        
        if load > 300:
            best = 'AWS'  # Scalable
            reason = "High load = AWS best for scaling"
        elif load < 100:
            best = 'GCP'  # Cheapest
            reason = "Low load = GCP cheapest option"
        else:
            best = 'Azure'  # Balanced
            reason = "Medium load = Azure balanced"
        
        current_cost = self.calculate_cost(self.current_provider, load)
        best_cost = self.calculate_cost(best, load)
        savings = current_cost - best_cost
        
        return {
            'current': self.current_provider,
            'suggested': best,
            'reason': reason,
            'savings_per_hour': savings,
            'savings_percent': int((savings/current_cost)*100) if current_cost > 0 else 0
        }
    
    def calculate_cost(self, provider, load):
        """Cost calculate karo"""
        base = 50  # Base cost
        factor = self.providers[provider]['cost_factor']
        return int(base * factor * (load / 100))
    
    def switch_cloud(self, new_provider):
        """Cloud switch karo"""
        old = self.current_provider
        self.current_provider = new_provider
        return f"☁️ Switched from {old} to {new_provider}!"
    
    def get_all_status(self):
        """Sab clouds ka status"""
        return {
            name: {
                'cost_per_100users': int(50 * info['cost_factor']),
                'speed': info['speed'],
                'color': info['color']
            }
            for name, info in self.providers.items()
        }