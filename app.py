import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Planning Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    h1, h2, h3 {
        color: #1f2937;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'sleep_data' not in st.session_state:
    st.session_state.sleep_data = []
if 'google_connected' not in st.session_state:
    st.session_state.google_connected = False
if 'hourly_rate' not in st.session_state:
    st.session_state.hourly_rate = 50

def add_task(title, priority, due_date):
    task = {
        'id': len(st.session_state.tasks) + 1,
        'title': title,
        'priority': priority,
        'due_date': str(due_date),
        'completed': False,
        'synced': False
    }
    st.session_state.tasks.append(task)

def toggle_task(task_id):
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break

def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task_id]

def add_sleep_entry(date, bedtime, waketime):
    bed = datetime.strptime(bedtime, '%H:%M')
    wake = datetime.strptime(waketime, '%H:%M')
    duration = (wake - bed).seconds / 3600
    if duration < 0:
        duration += 24
    
    entry = {
        'id': len(st.session_state.sleep_data) + 1,
        'date': str(date),
        'bedtime': bedtime,
        'waketime': waketime,
        'duration': round(duration, 1)
    }
    st.session_state.sleep_data.append(entry)

def get_sleep_quality(duration):
    if 7 <= duration <= 9:
        return "Optimal", "🟢", "#10b981"
    elif 6 <= duration < 7:
        return "Acceptable", "🟡", "#f59e0b"
    elif 5 <= duration < 6:
        return "Poor", "🟠", "#f97316"
    else:
        return "Critical", "🔴", "#ef4444"

def calculate_burnout_risk():
    if not st.session_state.sleep_data:
        return "Low", "🟢", "#10b981"
    
    avg_sleep = sum([s['duration'] for s in st.session_state.sleep_data]) / len(st.session_state.sleep_data)
    incomplete_tasks = len([t for t in st.session_state.tasks if not t['completed']])
    
    if avg_sleep < 6 and incomplete_tasks > 5:
        return "Critical", "🔴", "#ef4444"
    elif avg_sleep < 6.5 and incomplete_tasks > 4:
        return "High", "🟠", "#f97316"
    elif avg_sleep < 7 and incomplete_tasks > 3:
        return "Moderate", "🟡", "#f59e0b"
    else:
        return "Low", "🟢", "#10b981"

def display_logo():
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3em;'>📚 Planning Pro</h1>
    </div>
    """, unsafe_allow_html=True)

# User Type Selection
if st.session_state.user_type is None:
    display_logo()
    st.markdown("<p style='text-align: center; color: #6b7280; font-size: 1.3em;'>Smart Sleep & Task Management</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📚 Student", use_container_width=True, type="primary"):
                st.session_state.user_type = "student"
                st.rerun()
        with col_b:
            if st.button("💼 Professional", use_container_width=True):
                st.session_state.user_type = "professional"
                st.rerun()
    st.stop()

# Main App
st.markdown(f"# 📚 Planning Pro - {st.session_state.user_type.capitalize()} Mode")

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Navigation")
    
    if st.session_state.user_type == "student":
        tab_options = ["Tasks", "Sleep", "Analytics"]
    else:
        tab_options = ["Tasks", "Sleep", "Team", "Billing", "Analytics"]
    
    selected_tab = st.radio("", tab_options, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 🔗 Google Calendar")
    st.info("📌 Calendar sync available in local version")
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Tasks", len(st.session_state.tasks))
    st.metric("Completed", len([t for t in st.session_state.tasks if t['completed']]))
    
    st.markdown("---")
    if st.button("🔄 Switch User"):
        st.session_state.user_type = None
        st.rerun()

# Tasks Tab
if selected_tab == "Tasks":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ➕ Add New Task")
        task_title = st.text_input("📝 Task Title", key="task_input")
        col_a, col_b = st.columns(2)
        with col_a:
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        with col_b:
            due_date = st.date_input("Due Date")
        
        if st.button("Add Task", type="primary", use_container_width=True):
            if task_title:
                add_task(task_title, priority.lower(), due_date)
                st.success("✅ Task added!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 Your Tasks")
        
        if not st.session_state.tasks:
            st.info("No tasks yet!")
        else:
            for idx, task in enumerate(st.session_state.tasks):
                priority_colors = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
                emoji = priority_colors[task['priority']]
                
                col_check, col_task, col_del = st.columns([0.5, 4, 0.5])
                with col_check:
                    checked = st.checkbox("", value=task['completed'], key=f"c{task['id']}{idx}", label_visibility="collapsed")
                    if checked != task['completed']:
                        toggle_task(task['id'])
                        st.rerun()
                
                with col_task:
                    style = "text-decoration: line-through;" if task['completed'] else ""
                    st.markdown(f"<div style='background: white; padding: 15px; border-radius: 10px; {style}'><strong>{emoji} {task['title']}</strong><br><small>Due: {task['due_date']}</small></div>", unsafe_allow_html=True)
                
                with col_del:
                    if st.button("🗑️", key=f"d{task['id']}{idx}"):
                        delete_task(task['id'])
                        st.rerun()
    
    with col2:
        st.markdown("### 📊 Statistics")
        total = len(st.session_state.tasks)
        completed = len([t for t in st.session_state.tasks if t['completed']])
        high = len([t for t in st.session_state.tasks if t['priority'] == 'high' and not t['completed']])
        
        st.markdown(f"<div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 25px; border-radius: 15px; color: white; text-align: center;'><h3 style='color: white;'>Total</h3><h1 style='color: white;'>{total}</h1></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div style='background: linear-gradient(135deg, #f093fb, #f5576c); padding: 25px; border-radius: 15px; color: white; text-align: center;'><h3 style='color: white;'>High Priority</h3><h1 style='color: white;'>{high}</h1></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div style='background: linear-gradient(135deg, #4facfe, #00f2fe); padding: 25px; border-radius: 15px; color: white; text-align: center;'><h3 style='color: white;'>Completed</h3><h1 style='color: white;'>{completed}</h1></div>", unsafe_allow_html=True)

elif selected_tab == "Sleep":
    st.markdown("## 😴 Sleep Dashboard")
    
    if st.session_state.sleep_data:
        df = pd.DataFrame(st.session_state.sleep_data)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['date'], y=df['duration'], name='Sleep', marker_color='#8b5cf6'))
        fig.add_trace(go.Scatter(x=df['date'], y=[8]*len(df), name='Recommended', line=dict(color='#10b981', dash='dash')))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3, col4 = st.columns(4)
        avg = df['duration'].mean()
        with col1:
            st.metric("Avg Sleep", f"{avg:.1f}h")
        with col2:
            st.metric("Optimal", len(df[(df['duration'] >= 7) & (df['duration'] <= 9)]))
        with col3:
            st.metric("Max", f"{df['duration'].max():.1f}h")
        with col4:
            st.metric("Min", f"{df['duration'].min():.1f}h")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌙 Log Sleep")
        sleep_date = st.date_input("Date")
        col_a, col_b = st.columns(2)
        with col_a:
            bedtime = st.time_input("Bedtime", value=datetime.strptime("23:00", "%H:%M").time())
        with col_b:
            waketime = st.time_input("Wake Time", value=datetime.strptime("07:00", "%H:%M").time())
        
        if st.button("Log Entry", type="primary", use_container_width=True):
            add_sleep_entry(sleep_date, bedtime.strftime("%H:%M"), waketime.strftime("%H:%M"))
            st.success("✅ Logged!")
            st.rerun()
    
    with col2:
        st.markdown("### 📈 History")
        if st.session_state.sleep_data:
            for entry in st.session_state.sleep_data[-5:]:
                quality, emoji, color = get_sleep_quality(entry['duration'])
                st.markdown(f"<div style='background: white; padding: 15px; border-radius: 10px; border-left: 5px solid {color};'><strong>{entry['date']}</strong><br>{entry['bedtime']} → {entry['waketime']}<br><span style='font-size: 24px;'>{entry['duration']}h</span> {emoji} {quality}</div><br>", unsafe_allow_html=True)

elif selected_tab == "Team":
    st.markdown("## 👥 Team Wellness")
    team = [
        {'name': 'Sarah Johnson', 'tasks': 5, 'sleep': 7.2, 'status': 'warning'},
        {'name': 'Mike Chen', 'tasks': 3, 'sleep': 5.8, 'status': 'danger'},
        {'name': 'Emma Davis', 'tasks': 4, 'sleep': 8.1, 'status': 'ok'}
    ]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Members", len(team))
    with col2:
        st.metric("Critical", len([m for m in team if m['status'] == 'danger']))
    with col3:
        st.metric("Warning", len([m for m in team if m['status'] == 'warning']))
    
    st.markdown("---")
    for m in team:
        config = {'ok': ('🟢', 'Healthy', '#10b981'), 'warning': ('🟡', 'At Risk', '#f59e0b'), 'danger': ('🔴', 'Critical', '#ef4444')}
        emoji, label, color = config[m['status']]
        st.markdown(f"<div style='background: white; padding: 20px; border-radius: 12px; border-left: 5px solid {color};'><h3>{m['name']} {emoji} {label}</h3><p>📋 {m['tasks']} tasks | 😴 {m['sleep']}h sleep</p></div><br>", unsafe_allow_html=True)

elif selected_tab == "Billing":
    st.markdown("## 💰 Billing")
    st.session_state.hourly_rate = st.number_input("Hourly Rate", value=st.session_state.hourly_rate, min_value=10)
    
    col1, col2, col3 = st.columns(3)
    hours = len(st.session_state.tasks) * 2
    earnings = hours * st.session_state.hourly_rate
    
    with col1:
        st.metric("Hours", f"{hours}h")
    with col2:
        st.metric("Rate", f"${st.session_state.hourly_rate}")
    with col3:
        st.metric("Earnings", f"${earnings}")
    
    if st.button("Generate Invoice", type="primary"):
        st.balloons()
        st.success(f"Invoice: ${earnings}")

elif selected_tab == "Analytics":
    st.markdown("## 📊 Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.tasks:
            completed = len([t for t in st.session_state.tasks if t['completed']])
            pending = len(st.session_state.tasks) - completed
            fig = go.Figure(data=[go.Pie(labels=['Completed', 'Pending'], values=[completed, pending], hole=.4, marker_colors=['#10b981', '#ef4444'])])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if st.session_state.sleep_data:
            df = pd.DataFrame(st.session_state.sleep_data)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=df['duration'], mode='lines+markers', line=dict(color='#8b5cf6', width=3)))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    risk, emoji, color = calculate_burnout_risk()
    st.markdown(f"<div style='background: {color}; padding: 30px; border-radius: 20px; color: white; text-align: center;'><h2 style='color: white;'>Burnout Risk</h2><h1 style='color: white; font-size: 3em;'>{emoji} {risk}</h1></div>", unsafe_allow_html=True)