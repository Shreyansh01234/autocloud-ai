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

# Premium dashboard theme
st.markdown("""
<style>
    :root {
        color-scheme: dark;
        --canvas: #080d17;
        --surface: rgba(16, 24, 39, 0.82);
        --surface-raised: rgba(22, 32, 51, 0.92);
        --line: rgba(148, 163, 184, 0.15);
        --muted: #91a0b7;
        --text: #edf4ff;
        --cyan: #45d6e8;
        --violet: #9b8cff;
        --green: #5de0a0;
        --shadow: 0 18px 48px rgba(0, 0, 0, 0.22);
    }

    .stApp {
        color: var(--text);
        background:
            radial-gradient(ellipse at 12% 0%, rgba(38, 113, 150, 0.17), transparent 34%),
            radial-gradient(ellipse at 88% 8%, rgba(102, 75, 171, 0.15), transparent 30%),
            var(--canvas);
        font-family: Inter, "Segoe UI", sans-serif;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stHeader"] {
        height: 2.5rem;
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 1720px;
        padding: 2.25rem clamp(1.25rem, 3.5vw, 3.75rem) 3rem;
    }
    [data-testid="stAppViewContainer"] .main,
    [data-testid="stMarkdownContainer"] {
        color: var(--text);
    }
    .stMarkdown h3 {
        font-size: clamp(1rem, 1.35vw, 1.2rem);
        line-height: 1.35;
    }
    .stMarkdown h4 {
        font-size: clamp(0.85rem, 1.15vw, 1rem);
        line-height: 1.35;
    }

    .hero {
        position: relative;
        padding: 1rem 0 1.35rem;
        animation: rise-in 650ms ease-out both;
    }
    .hero-kicker {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.7rem;
        color: #9eacc2;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }
    .live-dot {
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 14px rgba(93, 224, 160, 0.8);
        animation: breathe 2.4s ease-in-out infinite;
    }
    .main-header {
        margin: 0;
        color: var(--text);
        font-size: clamp(2.2rem, 4vw, 3.35rem);
        font-weight: 750;
        letter-spacing: -0.055em;
        line-height: 1.08;
    }
    .main-header span {
        background: linear-gradient(100deg, #eef5ff 8%, #8bdced 58%, #b5a3ff 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-description {
        margin: 0.7rem 0 0;
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.6;
    }
    .hero-rule {
        height: 1px;
        margin-top: 1.65rem;
        background: linear-gradient(90deg, rgba(69, 214, 232, 0.45), var(--line) 45%, transparent);
    }

    .metric-card {
        position: relative;
        height: 150px;
        min-height: 150px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
        padding: 1.1rem clamp(0.8rem, 1.3vw, 1.25rem);
        border: 1px solid var(--line);
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(24, 36, 57, 0.96), rgba(13, 20, 34, 0.9));
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.16), inset 0 1px rgba(255, 255, 255, 0.045);
        transition: transform 220ms ease, border-color 220ms ease, box-shadow 220ms ease;
        animation: rise-in 600ms ease-out both;
    }
    .metric-card::after {
        position: absolute;
        top: 0;
        right: 12%;
        left: 12%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(119, 207, 238, 0.6), transparent);
        content: "";
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(110, 208, 235, 0.36);
        box-shadow: 0 16px 34px rgba(0, 0, 0, 0.24), 0 0 25px rgba(69, 214, 232, 0.06);
    }
    .metric-card .metric-label {
        overflow: hidden;
        margin: 0;
        font-size: clamp(0.72rem, 0.9vw, 0.88rem);
        font-weight: 600;
        letter-spacing: 0.01em;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .metric-card .metric-value {
        margin-top: 0.6rem;
        font-size: clamp(1.55rem, 2.1vw, 2.1rem);
        font-weight: 700;
        letter-spacing: -0.045em;
        line-height: 1.15;
        white-space: nowrap;
    }
    .metric-trend {
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-width: 0;
        gap: 0.4rem;
        margin-top: 0.55rem;
    }
    .metric-trend > div {
        min-width: 0;
        flex: 1;
    }
    .metric-delta {
        font-size: 0.7rem;
        font-weight: 650;
        white-space: nowrap;
    }
    .metric-period {
        display: block;
        margin-top: 0.15rem;
        color: #8290a6;
        font-size: 0.58rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .metric-sparkline {
        width: 54px;
        height: 25px;
        flex: 0 0 54px;
        overflow: visible;
    }

    .st-key-alerts-panel,
    .st-key-health-panel {
        min-height: 410px;
        height: 100%;
        box-sizing: border-box;
        padding: 1rem 1.1rem;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: linear-gradient(155deg, rgba(20, 30, 48, 0.92), rgba(12, 19, 32, 0.92));
        box-shadow: var(--shadow), inset 0 1px rgba(255, 255, 255, 0.035);
        backdrop-filter: blur(12px);
        transition: border-color 220ms ease, transform 220ms ease;
    }
    .st-key-alerts-panel { border-color: rgba(248, 113, 113, 0.24); }
    .st-key-health-panel { border-color: rgba(69, 214, 232, 0.24); }
    .st-key-logs-panel {
        box-sizing: border-box;
        padding: 1rem 1.1rem;
        margin-top: 1.25rem;
        border: 1px solid rgba(93, 224, 160, 0.23);
        border-radius: 18px;
        background: linear-gradient(155deg, rgba(20, 30, 48, 0.92), rgba(12, 19, 32, 0.92));
        box-shadow: var(--shadow), inset 0 1px rgba(255, 255, 255, 0.035);
    }
    .alert-item {
        padding: 0.65rem 0.75rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(248, 113, 113, 0.16);
        border-left: 3px solid #f87171;
        border-radius: 10px;
        background: rgba(248, 113, 113, 0.07);
        animation: rise-in 300ms ease-out both;
    }
    .empty-alert-state {
        display: flex;
        min-height: 300px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.45rem;
        border: 1px solid rgba(93, 224, 160, 0.16);
        border-radius: 14px;
        background: linear-gradient(145deg, rgba(28, 89, 72, 0.2), rgba(11, 25, 30, 0.42));
        text-align: center;
    }
    .empty-alert-state strong {
        color: #9de7bd;
        font-size: 1.1rem;
    }
    .empty-alert-state span,
    .empty-alert-state small {
        color: #a7b5c8;
    }
    .log-entry {
        min-height: 2.8rem;
        display: flex;
        align-items: center;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(93, 224, 160, 0.12);
        border-radius: 10px;
        background: rgba(4, 10, 17, 0.48);
        font-family: "Cascadia Code", Consolas, monospace;
        font-size: 0.78rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    .ai-message {
        padding: 0.8rem 0.9rem;
        margin: 0.55rem 0;
        border: 1px solid rgba(69, 214, 232, 0.17);
        border-left: 3px solid var(--cyan);
        border-radius: 12px;
        background: linear-gradient(110deg, rgba(69, 214, 232, 0.09), rgba(155, 140, 255, 0.07));
        animation: rise-in 350ms ease-out both;
    }
    .st-key-health-panel [data-testid="stPlotlyChart"] {
        border: 0;
        background: transparent;
    }

    [data-testid="stButton"] > button {
        min-height: 2.65rem;
        border: 1px solid rgba(115, 190, 219, 0.2);
        border-radius: 11px;
        background: linear-gradient(120deg, rgba(47, 108, 139, 0.92), rgba(87, 76, 148, 0.92));
        color: #f5f8ff;
        font-weight: 650;
        box-shadow: 0 5px 16px rgba(0, 0, 0, 0.15);
        transition: transform 160ms ease, filter 160ms ease, box-shadow 160ms ease;
    }
    [data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        border-color: rgba(116, 218, 237, 0.52);
        filter: brightness(1.12);
        box-shadow: 0 8px 22px rgba(39, 142, 173, 0.18);
        color: #fff;
    }
    [data-testid="stButton"] > button:focus-visible,
    [data-testid="stTextInput"] input:focus-visible {
        outline: 2px solid var(--cyan);
        outline-offset: 3px;
    }
    [data-testid="stTextInput"] input {
        border: 1px solid var(--line);
        border-radius: 11px;
        background: rgba(6, 12, 22, 0.72);
        color: var(--text);
    }
    [data-testid="stTextInput"] input::placeholder {
        color: #8290a6;
    }
    [data-testid="stSlider"] [role="slider"] {
        box-shadow: 0 0 0 4px rgba(69, 214, 232, 0.12);
    }
    [data-testid="stExpander"] {
        border-color: var(--line);
        border-radius: 12px;
        background: rgba(7, 13, 23, 0.42);
    }
    [data-testid="stAlert"] {
        border-radius: 12px;
    }
    [data-testid="stMetric"] {
        padding: 0.65rem;
        border: 1px solid var(--line);
        border-radius: 12px;
        background: rgba(7, 13, 23, 0.45);
    }
    [data-testid="stPlotlyChart"] {
        overflow: hidden;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: rgba(10, 16, 27, 0.68);
    }
    hr {
        border-color: var(--line);
    }
    footer {
        visibility: hidden;
    }

    @keyframes rise-in {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes breathe {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.62; transform: scale(0.82); }
    }
    @media (max-width: 900px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1.5rem 1rem 2rem;
        }
        .hero {
            padding-top: 0.5rem;
        }
        .metric-card {
            height: 138px;
            min-height: 122px;
        }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            scroll-behavior: auto !important;
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
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
st.markdown("""
<div class="hero">
    <div class="hero-kicker"><span class="live-dot"></span> GenAIOps control plane · Simulation mode</div>
    <h1 class="main-header">☁️ <span>AutoCloud AI</span></h1>
    <p class="hero-description">Intelligent cloud operations, predictive insights, and multi-cloud cost control — in one clear view.</p>
    <div class="hero-rule"></div>
</div>
""", unsafe_allow_html=True)

# Get metrics
metrics = st.session_state.cloud.get_metrics()

# Override with manual load
if st.session_state.manual_load != 50:
    metrics['current_load'] = st.session_state.manual_load
    metrics['utilization'] = min(95, (st.session_state.manual_load / (metrics['servers'] * 100)) * 100)
    metrics['timestamp'] = datetime.now().strftime('%H:%M:%S')

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
    st.session_state.alerts = [
        existing for existing in st.session_state.alerts
        if existing['level'] != 'CRITICAL'
    ] + [alert]
else:
    st.session_state.alerts = [
        alert for alert in st.session_state.alerts
        if alert['level'] != 'CRITICAL'
    ]

if len(st.session_state.alerts) > 10:
    st.session_state.alerts = st.session_state.alerts[-10:]

def render_metric_card(title, value, display_value, history_values, accent, inverse=False):
    samples = history_values[-8:] + [value]
    reference_lag = min(5, len(samples) - 1)
    reference = samples[-(reference_lag + 1)]
    delta = ((value - reference) / abs(reference) * 100) if reference else 0

    if len(samples) < 3:
        delta_text = "Collecting trend data"
        delta_color = "#91a0b7"
    else:
        if abs(delta) < 0.05:
            delta_text = "Stable vs recent"
            delta_color = "#91a0b7"
        else:
            is_positive = delta > 0
            arrow = "↑" if is_positive else "↓"
            delta_text = f"{arrow} {abs(delta):.1f}%"
            delta_color = "#f87171" if (is_positive and inverse) or (not is_positive and not inverse) else "#5de0a0"

    low, high = min(samples), max(samples)
    spread = high - low or 1
    points = " ".join(
        f"{8 + index * 104 / max(1, len(samples) - 1):.1f},{21 - ((sample - low) / spread) * 16:.1f}"
        for index, sample in enumerate(samples)
    )
    sparkline = (
        f'<svg class="metric-sparkline" viewBox="0 0 120 26" aria-hidden="true">'
        f'<polyline points="{points}" fill="none" stroke="{accent}" '
        f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round" '
        f'opacity="0.9"/></svg>'
    )

    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label" style="color: {accent};">{title}</div>
            <div class="metric-value">{display_value}</div>
        </div>
        <div class="metric-trend">
            <div>
                <span class="metric-delta" style="color: {delta_color};">{delta_text}</span>
                <span class="metric-period">vs last {reference_lag} updates</span>
            </div>
            {sparkline}
        </div>
    </div>
    """, unsafe_allow_html=True)


history = st.session_state.cloud.get_history()
recent_history = history[-8:]
metric_columns = st.columns(5)
metric_cards = [
    ("🖥️ Servers", metrics['servers'], [entry['servers'] for entry in recent_history], "#45d6e8", False),
    ("👥 Active users", metrics['current_load'], [entry['current_load'] for entry in recent_history], "#5de0a0", False),
    ("📊 Utilization", metrics['utilization'], [entry['utilization'] for entry in recent_history], "#fbbf24", True),
    ("💰 Cost / hour", metrics['cost_per_hour'], [entry['cost_per_hour'] for entry in recent_history], "#f5a65b", True),
    ("🔮 Forecast", metrics['current_load'] * 1.2, [entry['current_load'] * 1.2 for entry in recent_history], "#9b8cff", False),
]
for column, (title, value, samples, accent, inverse) in zip(metric_columns, metric_cards):
    with column:
        display_value = f"{value:.1f}%" if title == "📊 Utilization" else f"₹{value:.0f}" if title == "💰 Cost / hour" else f"{value:.0f}"
        render_metric_card(title, value, display_value, samples, accent, inverse)

st.markdown("<br>", unsafe_allow_html=True)

# Main Layout - 3 Columns
left_col, mid_col, right_col = st.columns([1.6, 1, 1.3])

with left_col:
    chart_title_col, chart_range_col = st.columns([1.25, 1])
    with chart_title_col:
        st.markdown('<h3 style="color: #00d4ff;">📈 Live Monitoring</h3>', unsafe_allow_html=True)
    with chart_range_col:
        chart_window = st.selectbox(
            "Chart time range",
            ["15 min", "1 hour", "24 hours", "All session"],
            index=3,
            key="chart_window",
            label_visibility="collapsed"
        )

    history = st.session_state.cloud.get_history()
    now = datetime.now()
    chart_windows = {"15 min": 15, "1 hour": 60, "24 hours": 1440}
    if chart_window == "All session":
        chart_history = history
    else:
        cutoff = now - timedelta(minutes=chart_windows[chart_window])
        chart_history = []
        for entry in history:
            sample_time = datetime.combine(
                now.date(),
                datetime.strptime(entry['timestamp'], "%H:%M:%S").time()
            )
            if sample_time > now + timedelta(minutes=1):
                sample_time -= timedelta(days=1)
            if sample_time >= cutoff:
                chart_history.append(entry)

    if chart_history:
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Traffic Load vs Capacity', 'Server Utilization %'),
            vertical_spacing=0.15
        )
        
        times = [h['timestamp'] for h in chart_history]
        loads = [h['current_load'] for h in chart_history]
        capacities = [h['capacity'] for h in chart_history]
        utils = [h['utilization'] for h in chart_history]
        
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
    else:
        st.info("No readings in this time range yet. Keep the dashboard open to collect telemetry.")

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

    demo_scenarios = {
        "Custom traffic": None,
        "Normal traffic · 120 users": 120,
        "Traffic spike · 500 users": 500,
        "Low traffic · 35 users": 35,
    }
    selected_scenario = st.selectbox(
        "Demo scenario",
        list(demo_scenarios),
        key="demo_scenario"
    )
    if st.button(
        "🎬 Apply demo scenario",
        use_container_width=True,
        disabled=demo_scenarios[selected_scenario] is None
    ):
        st.session_state.manual_load = demo_scenarios[selected_scenario]
        st.rerun()
    st.caption("Simulation only · No real cloud resources are changed.")
    
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

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<h3 style="color: #edf4ff;">Operations &amp; system health</h3>', unsafe_allow_html=True)
st.caption("Live alerts, resource health, and recent activity at a glance.")

alerts_col, health_col = st.columns(2, gap="large")

with alerts_col:
    with st.container(border=True, key="alerts-panel"):
        st.markdown('<h4 style="color: #f87171; margin-top: 0;">🔔 Live Alerts</h4>', unsafe_allow_html=True)
        if st.session_state.alerts:
            for alert in reversed(st.session_state.alerts[-4:]):
                st.markdown(f"""
                <div class="alert-item">
                    <b style="color: {alert['color']}">[{alert['level']}]</b>
                    <span style="color: #aab8cb;">{alert['time']}</span><br>
                    <span>{alert['msg']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-alert-state">
                <span>✓</span>
                <strong>All systems clear</strong>
                <small>There are no active alerts right now.</small>
            </div>
            """, unsafe_allow_html=True)

with health_col:
    with st.container(border=True, key="health-panel"):
        st.markdown('<h4 style="color: #45d6e8; margin-top: 0;">🎯 System Health</h4>', unsafe_allow_html=True)

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
            fillcolor='rgba(69,214,232,0.2)',
            line=dict(color='#45d6e8', width=2),
            name='Health'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(148,163,184,0.18)'),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            height=285,
            margin=dict(l=35, r=35, t=24, b=24)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        avg_health = int(sum(values) / len(values))
        health_color = '#5de0a0' if avg_health > 80 else '#fbbf24' if avg_health > 60 else '#f87171'
        st.markdown(
            f'<h3 style="color: {health_color}; text-align: center; margin: 0;">{avg_health}% Healthy</h3>',
            unsafe_allow_html=True
        )

with st.container(border=True, key="logs-panel"):
    st.markdown('<h4 style="color: #5de0a0; margin-top: 0;">⚡ System Logs</h4>', unsafe_allow_html=True)
    log_columns = st.columns(2, gap="large")
    for index, log in enumerate(reversed(st.session_state.system_logs[-10:])):
        if 'CRITICAL' in log or 'ERROR' in log:
            color = '#f87171'
        elif 'WARNING' in log:
            color = '#fbbf24'
        else:
            color = '#9de7bd'
        with log_columns[index % 2]:
            st.markdown(
                f'<div class="log-entry" style="color: {color}">{log}</div>',
                unsafe_allow_html=True
            )

st.markdown("<br>", unsafe_allow_html=True)
with st.container(border=True):
    st.markdown('<h3 style="color: #edf4ff; margin-top: 0;">⚙️ Scaling controls</h3>', unsafe_allow_html=True)
    mode_col, action_col = st.columns([1, 2], gap="large")
    with mode_col:
        auto_mode = st.toggle("🤖 Autonomous mode", st.session_state.auto_mode)
        st.session_state.auto_mode = auto_mode
        if auto_mode:
            st.success("AI autopilot is active.")
        else:
            st.caption("Manual mode · Review actions before scaling.")

    if auto_mode:
        decision, level = st.session_state.ai.analyze(metrics)
        with st.spinner("🧠 AI analyzing current load..."):
            time.sleep(0.5)

        st.session_state.decision_history.append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'decision': decision,
            'load': metrics['current_load'],
            'servers': metrics['servers']
        })

        with action_col:
            if metrics['utilization'] > 80 and not st.session_state.ai_triggered:
                st.error("🚨 Critical utilization detected. Emergency scaling in progress.")
                st.balloons()
                st.session_state.ai_triggered = True
                result = st.session_state.cloud.scale_up()
                st.success(f"✅ AI action: {result}")
                st.info(st.session_state.ai.get_smart_reply(decision, level, metrics))
                time.sleep(2)
                st.session_state.ai_triggered = False
                st.rerun()
            elif decision == 'scale_up':
                st.warning(st.session_state.ai.get_smart_reply(decision, level, metrics))
            elif decision == 'scale_down':
                st.success(st.session_state.ai.get_smart_reply(decision, level, metrics))
            else:
                st.info("✅ System stable. AI monitoring continues.")
    else:
        with action_col:
            scale_up_col, scale_down_col = st.columns(2, gap="medium")
            with scale_up_col:
                if st.button("🚀 Scale up", use_container_width=True):
                    result = st.session_state.cloud.scale_up()
                    st.success(result)
                    st.balloons()
            with scale_down_col:
                if st.button("📉 Scale down", use_container_width=True):
                    result = st.session_state.cloud.scale_down()
                    st.success(result)

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">🎓 Minor Project | GenAIOps Framework | AutoCloud AI</p>', unsafe_allow_html=True)

# Auto refresh
if time.time() - st.session_state.last_update > 2:
    st.session_state.last_update = time.time()
    if st.session_state.auto_mode:
        st.rerun()