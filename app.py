import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import random

from components.cloud_simulator import CloudSimulator
from components.ai_engine import AIEngine

# Page Setup
st.set_page_config(
    page_title="AutoCloud AI | GenAIOps",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Theme CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #00d4ff, #7b2cbf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00d4ff;
        box-shadow: 0 4px 15px rgba(0,212,255,0.3);
    }
    .alert-panel {
        background: linear-gradient(135deg, #ff444420, #ff880020);
        border: 2px solid #ff4444;
        border-radius: 15px;
        padding: 15px;
        max-height: 200px;
        overflow-y: auto;
    }
    .alert-item {
        background: rgba(255,68,68,0.2);
        border-left: 4px solid #ff4444;
        padding: 8px;
        margin: 5px 0;
        border-radius: 5px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .log-stream {
        background: #0a0a0a;
        border: 1px solid #00ff88;
        border-radius: 10px;
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #00ff88;
        max-height: 150px;
        overflow-y: auto;
    }
    .log-entry {
        margin: 2px 0;
        border-bottom: 1px dotted #333;
    }
    .predict-panel {
        background: linear-gradient(135deg, #7b2cbf20, #00d4ff20);
        border: 2px solid #7b2cbf;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .cost-panel {
        background: linear-gradient(135deg, #00ff8820, #00d4ff20);
        border: 2px solid #00ff88;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .cloud-panel {
        background: linear-gradient(135deg, #ff990020, #4285f420);
        border: 2px solid #ff9900;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .traffic-panel {
        background: linear-gradient(135deg, #ff444420, #ff880020);
        border: 2px solid #ff4444;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .timeline-panel {
        background: linear-gradient(135deg, #00d4ff20, #7b2cbf20);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 15px;
    }
    .chat-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 20px;
        border: 2px solid #00d4ff;
    }
    .ai-message {
        background: linear-gradient(90deg, #00d4ff20, #7b2cbf20);
        border-left: 4px solid #00d4ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: slideIn 0.5s ease;
    }
    @keyframes slideIn {
        from {opacity: 0; transform: translateX(-20px);}
        to {opacity: 1; transform: translateX(0);}
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff, #7b2cbf);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-weight: bold;
    }
    .health-radar {
        background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, rgba(0,0,0,0) 70%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize
if 'cloud' not in st.session_state:
    st.session_state.cloud = CloudSimulator()
    st.session_state.ai = AIEngine()
    st.session_state.auto_mode = False
    st.session_state.chat_history = []
    st.session_state.last_update = time.time()
    st.session_state.manual_load = 50
    st.session_state.ai_triggered = False
    st.session_state.alerts = []
    st.session_state.decision_history = []
    st.session_state.system_logs = []

# Header
st.markdown('<h1 class="main-header">☁️ AutoCloud AI</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #00d4ff;">🤖 Generative AI + Predictive + Multi-Cloud + Smart Alerts</h3>', unsafe_allow_html=True)

# Get metrics
metrics = st.session_state.cloud.get_metrics()

# Override with manual load
if st.session_state.manual_load != 50:
    metrics['current_load'] = st.session_state.manual_load
    metrics['utilization'] = min(95, (st.session_state.manual_load / (metrics['servers'] * 100)) * 100)

# Generate system logs
log_messages = [
    "[INFO] Monitoring active...",
    "[INFO] CPU usage normal",
    "[INFO] Memory optimized",
    "[INFO] Network stable",
    "[INFO] Backup completed",
    f"[DATA] Load: {metrics['current_load']} users",
    f"[DATA] Servers: {metrics['servers']} active",
]
st.session_state.system_logs.append(random.choice(log_messages))
if len(st.session_state.system_logs) > 20:
    st.session_state.system_logs = st.session_state.system_logs[-20:]

# Generate alerts based on conditions
if metrics['utilization'] > 80:
    alert = {
        'time': datetime.now().strftime('%H:%M:%S'),
        'level': 'CRITICAL',
        'msg': f"High utilization: {metrics['utilization']:.1f}%!",
        'color': '#ff4444'
    }
    if alert not in st.session_state.alerts[-3:]:
        st.session_state.alerts.append(alert)

if len(st.session_state.alerts) > 10:
    st.session_state.alerts = st.session_state.alerts[-10:]

# Top Metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: #00d4ff; margin: 0;">🖥️ Servers</h4>
        <h2 style="color: white; margin: 0; font-size: 2.5rem;">{metrics['servers']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: #00ff88; margin: 0;">👥 Users</h4>
        <h2 style="color: white; margin: 0; font-size: 2.5rem;">{metrics['current_load']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    util_color = "#ff4444" if metrics['utilization'] > 80 else "#ffaa00" if metrics['utilization'] > 60 else "#00ff88"
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: {util_color}; margin: 0;">📊 Utilization</h4>
        <h2 style="color: white; margin: 0; font-size: 2.5rem;">{metrics['utilization']:.1f}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: #ffaa00; margin: 0;">💰 Cost/hr</h4>
        <h2 style="color: white; margin: 0; font-size: 2.5rem;">₹{metrics['cost_per_hour']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: #7b2cbf; margin: 0;">🔮 Predicted</h4>
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">{int(metrics['current_load'] * 1.2)}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Layout - 3 Columns
left_col, mid_col, right_col = st.columns([2, 1, 1])

with left_col:
    # Live Graphs
    st.markdown('<h3 style="color: #00d4ff;">📈 Live Monitoring</h3>', unsafe_allow_html=True)
    
    history = st.session_state.cloud.get_history()
    
    if len(history) > 1:
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Traffic Load vs Capacity', 'Server Utilization %'),
            vertical_spacing=0.15
        )
        
        times = [h['timestamp'] for h in history]
        loads = [h['current_load'] for h in history]
        capacities = [h['capacity'] for h in history]
        utils = [h['utilization'] for h in history]
        
        # Add current point
        if st.session_state.manual_load != 50:
            times.append(datetime.now().strftime('%H:%M:%S'))
            loads.append(st.session_state.manual_load)
            capacities.append(metrics['capacity'])
            utils.append(metrics['utilization'])
        
        # Load vs Capacity
        fig.add_trace(
            go.Scatter(x=times, y=loads, name='Traffic', 
                      line=dict(color='#ff4444', width=3),
                      fill='tozeroy', fillcolor='rgba(255,68,68,0.2)'),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=times, y=capacities, name='Capacity',
                      line=dict(color='#00ff88', width=3, dash='dash')),
            row=1, col=1
        )
        
        # Utilization
        colors = ['#ff4444' if u > 80 else '#ffaa00' if u > 60 else '#00ff88' for u in utils]
        fig.add_trace(
            go.Scatter(x=times, y=utils, name='Utilization %',
                      line=dict(color='#00d4ff', width=3),
                      marker=dict(color=colors, size=10)),
            row=2, col=1
        )
        
        fig.add_hline(y=80, line_dash="dash", line_color="red", row=2, col=1)
        
        fig.update_layout(
            height=400,
            showlegend=True,
            plot_bgcolor='#0f0f23',
            paper_bgcolor='#0f0f23',
            font=dict(color='white'),
            legend=dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='#00d4ff', borderwidth=1)
        )
        
        fig.update_xaxes(gridcolor='#333', tickangle=45)
        fig.update_yaxes(gridcolor='#333')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # BOTTOM SECTION - 3 Panels
    st.markdown("<br>", unsafe_allow_html=True)
    
    bot_col1, bot_col2, bot_col3 = st.columns(3)
    
    # 🔔 ALERT PANEL
    with bot_col1:
        st.markdown('<div class="alert-panel">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #ff4444; margin: 0;">🔔 Live Alerts</h4>', unsafe_allow_html=True)
        
        if st.session_state.alerts:
            for alert in reversed(st.session_state.alerts[-5:]):
                st.markdown(f"""
                <div class="alert-item">
                    <b style="color: {alert['color']}">[{alert['level']}]</b> {alert['time']}<br>
                    <small>{alert['msg']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("✅ No active alerts")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 📊 SYSTEM HEALTH RADAR
    with bot_col2:
        st.markdown('<div class="health-radar" style="border: 2px solid #00d4ff; border-radius: 15px; padding: 15px;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #00d4ff; margin: 0; text-align: center;">🎯 System Health</h4>', unsafe_allow_html=True)
        
        # Radar chart
        categories = ['CPU', 'Memory', 'Network', 'Storage', 'Security']
        values = [
            min(100, metrics['cpu_percent']),
            min(100, metrics['memory_percent']),
            random.randint(70, 95),
            random.randint(80, 98),
            random.randint(85, 100)
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(0,212,255,0.3)',
            line=dict(color='#00d4ff', width=2),
            name='Health'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#333'),
                bgcolor='#0f0f23'
            ),
            showlegend=False,
            paper_bgcolor='#0f0f23',
            font=dict(color='white'),
            height=200,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Health score
        avg_health = int(sum(values) / len(values))
        health_color = '#00ff88' if avg_health > 80 else '#ffaa00' if avg_health > 60 else '#ff4444'
        st.markdown(f'<h3 style="color: {health_color}; text-align: center; margin: 0;">{avg_health}% Healthy</h3>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ⚡ LOG STREAM
    with bot_col3:
        st.markdown('<div style="border: 2px solid #00ff88; border-radius: 15px; padding: 15px; background: #0a0a0a;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #00ff88; margin: 0;">⚡ System Logs</h4>', unsafe_allow_html=True)
        
        log_html = '<div class="log-stream">'
        for log in reversed(st.session_state.system_logs[-8:]):
            if 'CRITICAL' in log or 'ERROR' in log:
                color = '#ff4444'
            elif 'WARNING' in log:
                color = '#ffaa00'
            else:
                color = '#00ff88'
            log_html += f'<div class="log-entry" style="color: {color}">{log}</div>'
        log_html += '</div>'
        
        st.markdown(log_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto Mode
    st.markdown("<br>", unsafe_allow_html=True)
    auto_mode = st.toggle("🤖 **AUTONOMOUS MODE**", st.session_state.auto_mode)
    st.session_state.auto_mode = auto_mode
    
    if auto_mode:
        st.success("🚀 AI AUTOPILOT ON!")
        
        decision, level = st.session_state.ai.analyze(metrics)
        
        with st.spinner("🧠 AI soch raha hai..."):
            time.sleep(0.5)
        
        # Save decision to history
        st.session_state.decision_history.append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'decision': decision,
            'load': metrics['current_load'],
            'servers': metrics['servers']
        })
        
        if metrics['utilization'] > 80 and not st.session_state.ai_triggered:
            st.error("🚨 CRITICAL! AI taking emergency action!")
            st.balloons()
            st.session_state.ai_triggered = True
            
            result = st.session_state.cloud.scale_up()
            st.success(f"✅ AI ACTION: {result}")
            
            reply = st.session_state.ai.get_smart_reply(decision, level, metrics)
            st.info(reply)
            
            time.sleep(2)
            st.session_state.ai_triggered = False
            st.rerun()
        
        elif decision == 'scale_up':
            reply = st.session_state.ai.get_smart_reply(decision, level, metrics)
            st.warning(reply)
        elif decision == 'scale_down':
            reply = st.session_state.ai.get_smart_reply(decision, level, metrics)
            st.success(reply)
        else:
            st.info("✅ AI: System stable. Monitoring...")
    else:
        st.warning("👤 MANUAL MODE")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 SCALE UP", use_container_width=True):
                result = st.session_state.cloud.scale_up()
                st.success(result)
                st.balloons()
        
        with c2:
            if st.button("📉 SCALE DOWN", use_container_width=True):
                result = st.session_state.cloud.scale_down()
                st.success(result)

with mid_col:
    # 🔮 PREDICTIVE AI
    st.markdown('<div class="predict-panel">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #7b2cbf; text-align: center;">🔮 AI Predictor</h3>', unsafe_allow_html=True)
    
    history = st.session_state.cloud.get_history()
    prediction = st.session_state.ai.predict_future(history)
    
    if isinstance(prediction, dict):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.metric("Trend", prediction['trend'])
        with col_p2:
            st.metric("Confidence", f"{prediction['confidence']}%")
        
        st.info(f"🕐 By {prediction['time']}: ~{prediction['prediction']} users")
        
        if prediction['action'] == 'scale_up':
            st.warning("⚠️ Prepare for scaling!")
        elif prediction['action'] == 'scale_down':
            st.success("💰 Save costs soon!")
    else:
        st.caption(prediction)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 🎯 AI DECISION TIMELINE
    st.markdown('<div class="timeline-panel">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #00d4ff; text-align: center;">🎯 AI Decision History</h4>', unsafe_allow_html=True)
    
    if st.session_state.decision_history:
        for dec in reversed(st.session_state.decision_history[-5:]):
            emoji = '🚀' if dec['decision'] == 'scale_up' else '📉' if dec['decision'] == 'scale_down' else '✅'
            color = '#ff4444' if dec['decision'] == 'scale_up' else '#00ff88' if dec['decision'] == 'scale_down' else '#00d4ff'
            st.markdown(f"""
            <div style="border-left: 3px solid {color}; padding-left: 10px; margin: 5px 0; font-size: 12px;">
                <b style="color: {color}">{emoji} {dec['time']}</b><br>
                <small>{dec['decision'].upper()} | Load: {dec['load']} | Servers: {dec['servers']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No decisions yet...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 💰 COST OPTIMIZER
    st.markdown('<div class="cost-panel">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #00ff88; text-align: center;">💰 Cost Optimizer</h3>', unsafe_allow_html=True)
    
    insights = st.session_state.cloud.get_cost_insights()
    
    st.metric("Daily Cost", f"₹{insights['current_daily']}")
    
    if insights['potential_savings'] > 0:
        st.success(f"💡 Save ₹{insights['potential_savings']}/day!")
        st.caption(f"Tip: {insights['recommendation']}")
    else:
        st.info("✅ Already optimized!")
    
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    # 🌐 MULTI-CLOUD
    st.markdown('<div class="cloud-panel">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #ff9900; text-align: center;">☁️ Multi-Cloud AI</h3>', unsafe_allow_html=True)
    
    if 'multicloud' not in st.session_state:
        from components.multi_cloud import MultiCloudManager
        st.session_state.multicloud = MultiCloudManager()
    
    mc = st.session_state.multicloud
    suggestion = mc.get_best_provider(st.session_state.manual_load)
    
    st.caption(f"Current: **{suggestion['current']}**")
    
    if suggestion['suggested'] != suggestion['current']:
        st.warning(f"🤖 Switch to **{suggestion['suggested']}**!")
        st.success(f"Save {suggestion['savings_percent']}%!")
        st.caption(suggestion['reason'])
        
        if st.button(f"☁️ Switch to {suggestion['suggested']}", key="switch_cloud"):
            result = mc.switch_cloud(suggestion['suggested'])
            st.success(result)
            st.balloons()
    else:
        st.success("✅ Best cloud selected!")
    
    with st.expander("📊 Compare All Clouds"):
        all_clouds = mc.get_all_status()
        for name, info in all_clouds.items():
            st.markdown(f"""
            <div style="background: {info['color']}30; padding: 8px; border-radius: 5px; margin: 5px 0;">
                <b style="color: {info['color']}">{name}</b>: ₹{info['cost_per_100users']}/100users
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 🎮 TRAFFIC CONTROL
    st.markdown('<div class="traffic-panel">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #ff4444; text-align: center;">🎮 Traffic Control</h3>', unsafe_allow_html=True)
    
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("50", key="btn_50"):
            st.session_state.manual_load = 50
            st.rerun()
    with b2:
        if st.button("150", key="btn_150"):
            st.session_state.manual_load = 150
            st.rerun()
    with b3:
        if st.button("🔥 300", key="btn_300"):
            st.session_state.manual_load = 300
            st.rerun()
    with b4:
        if st.button("💥 500", key="btn_500"):
            st.session_state.manual_load = 500
            st.rerun()
    
    manual_load = st.slider("Custom:", 10, 600, st.session_state.manual_load)
    if manual_load != st.session_state.manual_load:
        st.session_state.manual_load = manual_load
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 💬 CHAT
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #00d4ff; text-align: center;">💬 AI Assistant</h3>', unsafe_allow_html=True)
    
    chat_container = st.container(height=180)
    with chat_container:
        for msg in st.session_state.chat_history[-4:]:
            if msg['type'] == 'user':
                st.markdown(f"<div style='text-align: right; color: #00d4ff;'>👤 {msg['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ai-message'>🤖 {msg['text']}</div>", unsafe_allow_html=True)
    
    user_input = st.text_input("Command:", placeholder="'predict', 'optimize', 'cloud'", key="chat_input")
    
    if st.button("Send", use_container_width=True):
        if user_input:
            st.session_state.chat_history.append({'type': 'user', 'text': user_input})
            
            msg_lower = user_input.lower()
            response = ""
            
            if 'predict' in msg_lower:
                pred = st.session_state.ai.predict_future(st.session_state.cloud.get_history())
                if isinstance(pred, dict):
                    response = f"🔮 {pred['trend']}! By {pred['time']}: ~{pred['prediction']} users. Confidence: {pred['confidence']}%"
                else:
                    response = pred
                    
            elif 'optimize' in msg_lower or 'cost' in msg_lower:
                opt = st.session_state.cloud.get_cost_insights()
                response = f"💰 Daily: ₹{opt['current_daily']}. {opt['recommendation']}! Save ₹{opt['potential_savings']}/day"
                
            elif 'cloud' in msg_lower or 'aws' in msg_lower or 'azure' in msg_lower or 'gcp' in msg_lower:
                mc = st.session_state.multicloud
                sg = mc.get_best_provider(st.session_state.manual_load)
                response = f"☁️ Current: {sg['current']}. Best: {sg['suggested']}. Reason: {sg['reason']}. Save {sg['savings_percent']}%!"
                
            else:
                action, response = st.session_state.ai.chat(user_input)
                if action == 'scale_up':
                    st.session_state.cloud.scale_up()
                    response += f"\n✅ Servers: {st.session_state.cloud.servers}"
                elif action == 'scale_down':
                    result = st.session_state.cloud.scale_down()
                    response += f"\n{result}"
                elif action == 'status':
                    m = st.session_state.cloud.get_metrics()
                    response += f"\n📊 Servers: {m['servers']} | Load: {st.session_state.manual_load} | Util: {m['utilization']:.1f}%"
            
            st.session_state.chat_history.append({'type': 'ai', 'text': response})
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">🎓 Minor Project | GenAIOps Framework | AutoCloud AI</p>', unsafe_allow_html=True)

# Auto refresh
if time.time() - st.session_state.last_update > 2:
    st.session_state.last_update = time.time()
    if st.session_state.auto_mode:
        st.rerun()