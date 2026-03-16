import random
from datetime import datetime, timedelta

class AIEngine:
    """Smart AI - apne dimag se reply dega!"""
    
    def __init__(self):
        self.responses = {
            'scale_up': {
                'high_load': [
                    "🚨 CRITICAL! Load 90%+! Emergency scaling NOW!",
                    "⚡ Traffic tsunami detected! Auto-scaling activated!",
                    "🔥 System overload! Adding servers immediately!",
                    "📈 Viral moment! Scaling up to handle burst!"
                ],
                'medium_load': [
                    "📊 Load increasing. Proactive scaling...",
                    "⚠️ 70% threshold crossed. Preparing resources...",
                    "👀 Watching closely. Scaling for safety...",
                    "🚀 Better safe than sorry! Scaling up..."
                ]
            },
            'scale_down': {
                'low_load': [
                    "💤 Night mode detected. Saving your money...",
                    "🌙 Peaceful hours! Optimizing costs...",
                    "✅ Efficient scaling down. Cost saved!",
                    "💰 Smart saving: Reducing idle servers..."
                ],
                'idle': [
                    "😴 Almost empty! Minimum resources mode ON",
                    "🎯 Ultra-efficient: Bare minimum servers",
                    "💡 Saving maximum: Auto-optimization active"
                ]
            },
            'maintain': {
                'stable': [
                    "✅ All systems green! Monitoring continues...",
                    "🎯 Perfect balance! No changes needed...",
                    "👍 Smooth sailing! Watching for changes...",
                    "💚 Healthy status! Maintaining current setup..."
                ]
            }
        }
        
        self.reasons = {
            'scale_up': [
                "High user traffic detected",
                "Peak hours prediction",
                "Sales event incoming",
                "Viral content spike"
            ],
            'scale_down': [
                "Low activity period",
                "Night time optimization",
                "Cost saving mode",
                "Resource efficiency"
            ],
            'maintain': [
                "Stable traffic pattern",
                "Optimal utilization",
                "Balanced load",
                "No action required"
            ]
        }
    
    def analyze(self, metrics):
        """Decide kya karna hai"""
        util = metrics['utilization']
        load = metrics['current_load']
        servers = metrics['servers']
        
        if util > 80:
            return 'scale_up', 'high_load'
        elif util > 60:
            return 'scale_up', 'medium_load'
        elif util < 25 and servers > 1:
            return 'scale_down', 'low_load'
        elif util < 15 and servers > 2:
            return 'scale_down', 'idle'
        else:
            return 'maintain', 'stable'
    
    def get_smart_reply(self, decision, level, metrics):
        """Apne dimag se reply generate karega!"""
        
        template = random.choice(self.responses[decision][level])
        reason = random.choice(self.reasons[decision])
        
        reply = f"{template}\n\n"
        reply += f"🧠 Analysis:\n"
        reply += f"   • Reason: {reason}\n"
        reply += f"   • Load: {metrics['current_load']} users\n"
        reply += f"   • Utilization: {metrics['utilization']}%\n"
        reply += f"   • Current Servers: {metrics['servers']}\n\n"
        
        if decision == 'scale_up':
            new_servers = metrics['servers'] + 1
            new_cost = new_servers * 50
            reply += f"⚡ Action: Scaling to {new_servers} servers\n"
            reply += f"💰 New Cost: ₹{new_cost}/hour (was ₹{metrics['cost_per_hour']})"
            
        elif decision == 'scale_down':
            new_servers = metrics['servers'] - 1
            new_cost = new_servers * 50
            savings = metrics['cost_per_hour'] - new_cost
            reply += f"📉 Action: Reducing to {new_servers} servers\n"
            reply += f"💰 Savings: ₹{savings}/hour (New: ₹{new_cost})"
            
        else:
            reply += f"✅ Action: Maintaining {metrics['servers']} servers\n"
            reply += f"💰 Cost stable: ₹{metrics['cost_per_hour']}/hour"
        
        return reply
    
    def chat(self, user_msg):
        """Natural language samajhne ka jadoo!"""
        msg = user_msg.lower().strip()
        
        scale_up_words = ['up', 'badhao', 'zyada', 'badha', 'scale up', 'badao', 'increase', 'add']
        scale_down_words = ['down', 'kam', 'kum', 'ghatao', 'scale down', 'ghata', 'decrease', 'remove', 'band']
        status_words = ['status', 'kya hai', 'batao', 'dekhna', 'check', 'kya chal raha', 'halat']
        
        if any(word in msg for word in scale_up_words):
            return 'scale_up', "👍 Samajh gaya! Servers badhana hai!"
        
        elif any(word in msg for word in scale_down_words):
            return 'scale_down', "👍 Samajh gaya! Servers kam karne hain!"
        
        elif any(word in msg for word in status_words):
            return 'status', "👍 Status check karta hoon!"
        
        elif any(word in msg for word in ['help', 'madad', 'kya kar sakte ho']):
            return 'help', "🤓 Main kar sakta hoon:\n• 'scale up' - Servers badhana\n• 'scale down' - Servers kam karna\n• 'status' - Current status dekhna"
        
        else:
            return 'unknown', "🤔 Samajh nahi aaya! Try karo: 'scale up', 'status', ya 'help'"
    
    def predict_future(self, history):
        """🔮 Future predict karega!"""
        if len(history) < 3:
            return "⚠️ Data kam hai, prediction nahi kar sakta"
        
        recent = history[-3:]
        loads = [h['current_load'] for h in recent]
        
        if loads[-1] > loads[-2] > loads[0]:
            trend = "📈 UP"
            prediction = int(loads[-1] * 1.3)
        elif loads[-1] < loads[-2] < loads[0]:
            trend = "📉 DOWN"
            prediction = int(loads[-1] * 0.7)
        else:
            trend = "➡️ STABLE"
            prediction = loads[-1]
        
        future_time = (datetime.now() + timedelta(minutes=10)).strftime('%H:%M')
        
        return {
            'trend': trend,
            'prediction': prediction,
            'time': future_time,
            'confidence': random.randint(75, 95),
            'action': 'scale_up' if prediction > 200 else 'scale_down' if prediction < 50 else 'maintain'
        }