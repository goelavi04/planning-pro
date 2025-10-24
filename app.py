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

# Professional Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: #f8f9fa;
    }
    
    .block-container {
        padding: 2rem 3rem;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Headers */
    h1 {
        color: #1a202c;
        font-weight: 700;
        font-size: 2em;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.5em;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.2em;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border: 1.5px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 15px;
        transition: all 0.2s;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e9ecef;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Task item */
    .task-item {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 16px;
        margin: 10px 0;
        transition: all 0.2s;
    }
    
    .task-item:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
    }
    
    /* Sleep suggestions box */
    .suggestions-box {
        background: linear-gradient(135deg, #f3f4ff 0%, #e8e9ff 100%);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #667eea;
        margin: 20px 0;
    }
    
    .suggestion-item {
        color: #5a67d8;
        font-size: 14px;
        margin: 8px 0;
        padding-left: 20px;
        position: relative;
    }
    
    .suggestion-item:before {
        content: "•";
        position: absolute;
        left: 0;
        font-weight: bold;
    }
    
    /* Duration display */
    .duration-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);
    }
    
    .duration-number {
        font-size: 3em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }
    
    /* Remove default streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
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
        return "Good", "🟡", "#f59e0b"
    elif 5 <= duration < 6:
        return "Fair", "🟠", "#f97316"
    else:
        return "Poor", "🔴", "#ef4444"

def calculate_duration(bedtime, waketime):
    bed = datetime.strptime(bedtime, '%H:%M')
    wake = datetime.strptime(waketime, '%H:%M')
    duration = (wake - bed).seconds / 3600
    if duration < 0:
        duration += 24
    return round(duration, 1)

def get_smart_suggestions():
    return [
        "Adults need 7-9 hours for optimal performance",
        "Best bedtime: 10 PM - 11:30 PM for work productivity",
        "Maintain a regular sleep schedule for better energy",
        "Quality sleep improves decision-making by 30%"
    ]

# User Type Selection
if st.session_state.user_type is None:
    st.markdown("<div style='text-align: center; padding: 60px 0;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 3em; margin-bottom: 10px;'>📚 Planning Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.3em; color: #6b7280; margin-bottom: 40px;'>Smart Sleep & Task Management</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        if st.button("📚 Student Mode", use_container_width=True, type="primary"):
            st.session_state.user_type = "student"
            st.rerun()
        if st.button("💼 Professional Mode", use_container_width=True):
            st.session_state.user_type = "professional"
            st.rerun()
    st.stop()

# Main App Header
st.markdown(f"# Planning Pro")
st.markdown(f"<p style='color: #6b7280; font-size: 1.1em;'>{st.session_state.user_type.capitalize()} Mode • Smart Task & Sleep Management</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    
    if st.session_state.user_type == "student":
        tab_options = ["📋 Tasks", "😴 Sleep", "📊 Analytics"]
    else:
        tab_options = ["📋 Tasks", "😴 Sleep", "👥 Team", "💰 Billing", "📊 Analytics"]
    
    selected_tab = st.radio("", tab_options, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    total = len(st.session_state.tasks)
    completed = len([t for t in st.session_state.tasks if t['completed']])
    
    st.markdown(f"""
    <div class='metric-card'>
        <div style='color: #6b7280; font-size: 13px; font-weight: 500;'>TOTAL TASKS</div>
        <div style='font-size: 2em; font-weight: 700; color: #1a202c;'>{total}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-card'>
        <div style='color: #6b7280; font-size: 13px; font-weight: 500;'>COMPLETED</div>
        <div style='font-size: 2em; font-weight: 700; color: #10b981;'>{completed}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔄 Switch Mode", use_container_width=True):
        st.session_state.user_type = None
        st.rerun()

# Tasks Tab
if "📋 Tasks" in selected_tab:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Task Manager")
        st.markdown("<p style='color: #6b7280; margin-bottom: 20px;'>Organize and prioritize your tasks</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            task_title = st.text_input("Task Title", placeholder="Enter task name...", label_visibility="collapsed")
            
            col_a, col_b = st.columns(2)
            with col_a:
                priority = st.selectbox("Priority", ["High", "Medium", "Low"], label_visibility="collapsed")
            with col_b:
                due_date = st.date_input("Due Date", label_visibility="collapsed")
            
            if st.button("➕ Add Task", type="primary", use_container_width=True):
                if task_title:
                    add_task(task_title, priority.lower(), due_date)
                    st.success("✅ Task added successfully")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Filter tabs
        st.markdown("<div style='margin: 30px 0 20px 0;'>", unsafe_allow_html=True)
        filter_tab = st.radio("", ["All", "High", "Medium", "Low"], horizontal=True, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display tasks
        if not st.session_state.tasks:
            st.markdown("<div class='card' style='text-align: center; padding: 60px 20px;'><p style='color: #9ca3af; font-size: 1.1em;'>No tasks yet. Add your first task to get started!</p></div>", unsafe_allow_html=True)
        else:
            filtered_tasks = st.session_state.tasks
            if filter_tab != "All":
                filtered_tasks = [t for t in st.session_state.tasks if t['priority'] == filter_tab.lower()]
            
            for idx, task in enumerate(filtered_tasks):
                priority_colors = {
                    'high': ('#fee2e2', '#ef4444', '🔴'),
                    'medium': ('#fef3c7', '#f59e0b', '🟡'),
                    'low': ('#d1fae5', '#10b981', '🟢')
                }
                bg, border, emoji = priority_colors[task['priority']]
                
                col_check, col_task, col_del = st.columns([0.3, 4, 0.3])
                
                with col_check:
                    checked = st.checkbox("", value=task['completed'], key=f"c{task['id']}{idx}", label_visibility="collapsed")
                    if checked != task['completed']:
                        toggle_task(task['id'])
                        st.rerun()
                
                with col_task:
                    style = "text-decoration: line-through; opacity: 0.5;" if task['completed'] else ""
                    st.markdown(f"""
                    <div class='task-item' style='background: {bg}; border-left: 4px solid {border}; {style}'>
                        <div style='font-weight: 600; font-size: 15px; color: #1a202c; margin-bottom: 6px;'>
                            {emoji} {task['title']}
                        </div>
                        <div style='color: #6b7280; font-size: 13px;'>
                            📅 Due: {task['due_date']} • {task['priority'].capitalize()} Priority
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_del:
                    if st.button("🗑️", key=f"d{task['id']}{idx}"):
                        delete_task(task['id'])
                        st.rerun()
    
    with col2:
        st.markdown("### Overview")
        
        # Progress card
        if total > 0:
            progress = (completed / total) * 100
            st.markdown(f"""
            <div class='card'>
                <div style='color: #6b7280; font-size: 13px; font-weight: 500; margin-bottom: 12px;'>COMPLETION RATE</div>
                <div style='font-size: 2.5em; font-weight: 700; color: #667eea; margin-bottom: 8px;'>{int(progress)}%</div>
                <div style='background: #e9ecef; height: 8px; border-radius: 4px; overflow: hidden;'>
                    <div style='background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: {progress}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Priority breakdown
        high_count = len([t for t in st.session_state.tasks if t['priority'] == 'high' and not t['completed']])
        medium_count = len([t for t in st.session_state.tasks if t['priority'] == 'medium' and not t['completed']])
        low_count = len([t for t in st.session_state.tasks if t['priority'] == 'low' and not t['completed']])
        
        st.markdown(f"""
        <div class='card'>
            <div style='color: #1a202c; font-weight: 600; margin-bottom: 16px;'>Pending Tasks</div>
            <div style='margin: 12px 0;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 6px;'>
                    <span style='color: #6b7280; font-size: 14px;'>🔴 High Priority</span>
                    <span style='font-weight: 600;'>{high_count}</span>
                </div>
                <div style='display: flex; justify-content: space-between; margin-bottom: 6px;'>
                    <span style='color: #6b7280; font-size: 14px;'>🟡 Medium Priority</span>
                    <span style='font-weight: 600;'>{medium_count}</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='color: #6b7280; font-size: 14px;'>🟢 Low Priority</span>
                    <span style='font-weight: 600;'>{low_count}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Sleep Tab
elif "😴 Sleep" in selected_tab:
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### Sleep Schedule")
        st.markdown("<p style='color: #6b7280; margin-bottom: 20px;'>Optimize your rest for peak performance</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### 🌙 Bedtime")
                bedtime = st.time_input("Bedtime", value=datetime.strptime("22:00", "%H:%M").time(), label_visibility="collapsed")
            with col_b:
                st.markdown("#### ☀️ Wake Time")
                waketime = st.time_input("Wake Time", value=datetime.strptime("06:00", "%H:%M").time(), label_visibility="collapsed")
            
            duration = calculate_duration(bedtime.strftime("%H:%M"), waketime.strftime("%H:%M"))
            
            st.markdown(f"""
            <div class='duration-display'>
                <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>⏰ Sleep Duration</div>
                <div class='duration-number'>{duration} hours</div>
                <div style='font-size: 14px; opacity: 0.9;'>Target: 8 hours</div>
            </div>
            """, unsafe_allow_html=True)
            
            sleep_date = st.date_input("Date", label_visibility="collapsed")
            
            if st.button("💾 Save Schedule", type="primary", use_container_width=True):
                add_sleep_entry(sleep_date, bedtime.strftime("%H:%M"), waketime.strftime("%H:%M"))
                st.success("✅ Sleep schedule saved")
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Smart Suggestions
        st.markdown("""
        <div class='suggestions-box'>
            <div style='color: #5a67d8; font-weight: 600; font-size: 16px; margin-bottom: 12px;'>
                💡 Smart Suggestions for Professionals
            </div>
        """, unsafe_allow_html=True)
        
        for suggestion in get_smart_suggestions():
            st.markdown(f"<div class='suggestion-item'>{suggestion}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Sleep History")
        
        if st.session_state.sleep_data:
            for entry in st.session_state.sleep_data[-5:]:
                quality, emoji, color = get_sleep_quality(entry['duration'])
                st.markdown(f"""
                <div class='card'>
                    <div style='font-weight: 600; margin-bottom: 8px;'>{entry['date']}</div>
                    <div style='color: #6b7280; font-size: 14px; margin-bottom: 12px;'>
                        {entry['bedtime']} → {entry['waketime']}
                    </div>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='font-size: 1.8em; font-weight: 700;'>{entry['duration']}h</div>
                        <div style='color: {color}; font-weight: 600;'>{emoji} {quality}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No sleep data yet")

# Analytics, Team, Billing tabs (keeping them simple for now)
elif "📊 Analytics" in selected_tab:
    st.markdown("### Analytics Dashboard")
    if st.session_state.tasks:
        completed = len([t for t in st.session_state.tasks if t['completed']])
        pending = len(st.session_state.tasks) - completed
        fig = go.Figure(data=[go.Pie(
            labels=['Completed', 'Pending'],
            values=[completed, pending],
            hole=.5,
            marker_colors=['#10b981', '#ef4444']
        )])
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

elif "👥 Team" in selected_tab:
    st.markdown("### Team Dashboard")
    st.info("Team features coming soon")

elif "💰 Billing" in selected_tab:
    st.markdown("### Billing & Time Tracking")
    st.session_state.hourly_rate = st.number_input("Hourly Rate (USD)", value=st.session_state.hourly_rate, min_value=10)
    
    hours = len(st.session_state.tasks) * 2
    earnings = hours * st.session_state.hourly_rate
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Hours Tracked", f"{hours}h")
    with col2:
        st.metric("Hourly Rate", f"${st.session_state.hourly_rate}")
    with col3:
        st.metric("Total Earnings", f"${earnings}")