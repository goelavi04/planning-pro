import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date

# --- PAGE CONFIGURATION ---
# Use an emoji for a cleaner look. "✨" is a good option.
st.set_page_config(
    page_title="Planning Pro",
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL CUSTOM CSS ---
# Modern, clean UI with better spacing, fonts, and a professional color palette.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* --- General Styles --- */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #F0F2F6; /* Lighter gray background for a softer look */
    }
    
    .block-container {
        /* Add more padding for a spacious feel */
        padding: 2rem 3rem 3rem 3rem; 
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1a202c; /* Darker text for better contrast */
    }
    
    p {
        color: #4a5568; /* Slightly lighter for body text */
    }

    /* --- Custom UI Components --- */
    
    /* Card: The base for all components */
    .card {
        background: white;
        border-radius: 12px; /* Softer radius */
        padding: 24px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* Subtle shadow */
        border: 1px solid #E2E8F0; /* Light border */
        margin-bottom: 20px;
        transition: all 0.2s ease;
    }
    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Lift on hover */
        border-color: #CBD5E0;
    }
    
    /* Metric Card: For dashboard stats */
    .metric-card {
        text-align: left;
        padding: 20px;
    }
    .metric-card .label {
        color: #64748B; /* Muted label color */
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    .metric-card .value {
        font-size: 2.2em;
        font-weight: 700;
        color: #1E29B; /* Strong value color */
    }

    /* Task Item: Cleaner, more structured task display */
    .task-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px;
        margin: 10px 0;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        transition: all 0.2s;
    }
    .task-item:hover {
        background-color: #F8F9FA;
        border-color: #CBD5E0;
    }
    .task-item.completed {
        opacity: 0.6;
    }
    .task-item.completed .title {
        text-decoration: line-through;
    }
    .task-item-content {
        flex-grow: 1;
        margin: 0 15px;
    }
    .task-item .title {
        font-weight: 600;
        font-size: 15px;
        color: #334155;
    }
    .task-item .details {
        font-size: 13px;
        color: #64748B;
        margin-top: 4px;
    }
    
    /* Priority Badge */
    .priority-badge {
        font-size: 12px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
    }
    .priority-high { background-color: #FEE2E2; color: #DC2626; }
    .priority-medium { background-color: #FEF3C7; color: #D97706; }
    .priority-low { background-color: #D1FAE5; color: #059669; }

    /* Buttons: Primary action button */
    .stButton>button {
        background-color: #4F46E5; /* Darker Indigo for better contrast */
        color: white; /* Ensure button text is white */
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.2);
    }
    /* This new rule forces text/emojis inside buttons to be white */
    .stButton>button div[data-testid="stMarkdownContainer"] p {
        color: white !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        background-color: #4338CA; /* Even darker on hover */
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3);
    }
    .stButton>button:focus {
        background-color: #3730A3 !important; /* Darkest on focus */
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.4) !important;
    }

    /* REMOVED the broken :has() selector */
    
    .stButton>button:focus {
        background-color: #4F46E5 !important; /* Keep focus color consistent */
    }

    /* Delete Button: Subtle icon button */
    .stButton .delete-btn {
        background: transparent;
        color: #94A3B8;
        padding: 5px;
        font-size: 18px;
        box-shadow: none;
    }
    .stButton .delete-btn:hover {
        background: #F1F5F9;
        color: #EF4444;
        transform: none;
    }

    /* --- Sidebar --- */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    /* Sidebar Navigation Radio: Clean and modern */
    [data-testid="stSidebar"] .stRadio > div {
        border: 1px solid #E2E8F0;
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 10px;
    }
    [data-testid="stSidebar"] .stRadio [role="radio"] {
        background-color: white;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 5px 0;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] .stRadio [role="radio"]:hover {
        background-color: #F1F5F9;
    }
    [data-testid="stSidebar"] .stRadio [role="radio"] > div {
        color: #334155; /* Text color */
        font-weight: 500;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stDateInput>div>div>input, .stTimeInput>div>div>input {
        border: 1px solid #E2E8F0;
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 15px;
        transition: all 0.2s;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus, .stDateInput>div>div>input:focus, .stTimeInput>div>div>input:focus {
        border-color: #6366F1;
        background-color: #FFFFFF;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }

    /* --- Hide Streamlit Branding --- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
# Initialize state only if keys don't exist
def init_state(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

init_state('user_type', None)
init_state('tasks', [])
init_state('sleep_data', [])
init_state('google_connected', False)
init_state('hourly_rate', 50)

# --- DATA HANDLING FUNCTIONS ---
# These are your existing functions, slightly cleaned up for clarity

def add_task(title, priority, due_date):
    """Adds a new task to the session state."""
    # Use max() to avoid ID collision if tasks are deleted
    task_id = max([t['id'] for t in st.session_state.tasks] + [0]) + 1
    task = {
        'id': task_id,
        'title': title,
        'priority': priority,
        'due_date': str(due_date),
        'completed': False,
        'synced': False
    }
    st.session_state.tasks.append(task)
    st.toast(f"Task '{title}' added!", icon="🎉")

def toggle_task(task_id):
    """Toggles the completion status of a task."""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            status = "completed" if task['completed'] else "marked as pending"
            st.toast(f"Task '{task['title']}' {status}.", icon="✅" if task['completed'] else "⏳")
            break

def delete_task(task_id):
    """Removes a task from the session state."""
    st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task_id]
    st.toast("Task deleted.", icon="🗑️")

def add_sleep_entry(date, bedtime, waketime, duration):
    """Adds a new sleep entry to the session state."""
    entry_id = max([s['id'] for s in st.session_state.sleep_data] + [0]) + 1
    entry = {
        'id': entry_id,
        'date': str(date),
        'bedtime': bedtime,
        'waketime': waketime,
        'duration': duration
    }
    st.session_state.sleep_data.append(entry)
    st.toast(f"Sleep for {date} logged!", icon="😴")

# --- UI HELPER FUNCTIONS ---

def get_sleep_quality(duration):
    """Returns a quality rating and color based on sleep duration."""
    if 7 <= duration <= 9: return "Optimal", "#10B981"
    if 6 <= duration < 7: return "Good", "#F59E0B"
    if 5 <= duration < 6: return "Fair", "#F97316"
    return "Poor", "#EF4444"

def calculate_duration(bedtime, waketime):
    """Calculates sleep duration in hours, handling overnight wrapping."""
    bed = datetime.strptime(bedtime, '%H:%M')
    wake = datetime.strptime(waketime, '%H:%M')
    duration = (wake - bed).total_seconds() / 3600
    # Add 24 hours if duration is negative (overnight)
    return round(duration if duration >= 0 else duration + 24, 1)

def get_smart_suggestions():
    """Returns a list of static suggestions."""
    return [
        "Adults need 7-9 hours of sleep for optimal cognitive performance.",
        "A consistent bedtime (even on weekends) improves energy levels.",
        "Quality sleep is linked to a 30% improvement in decision-making.",
        "Try to get sunlight in the morning to regulate your circadian rhythm.",
    ]

def calculate_burnout_risk():
    """Calculates burnout risk based on sleep and task load."""
    if not st.session_state.sleep_data:
        return "Low", "#10B981"
    
    # Use pandas for easier mean calculation
    avg_sleep = pd.DataFrame(st.session_state.sleep_data)['duration'].mean()
    incomplete_tasks = sum(1 for t in st.session_state.tasks if not t['completed'])
    
    if avg_sleep < 6 and incomplete_tasks > 5: return "Critical", "#EF4444"
    if avg_sleep < 6.5 and incomplete_tasks > 4: return "High", "#F97316"
    if avg_sleep < 7 and incomplete_tasks > 3: return "Moderate", "#F59E0B"
    return "Low", "#10B981"

# --- 1. WELCOME PAGE ---

def render_welcome_page():
    """Displays the initial user type selection screen."""
    st.markdown("<div style='text-align: center; padding: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 3.5em; font-weight: 700;'>Welcome to Planning Pro ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.3em; color: #4a5568; max-width: 600px; margin: 20px auto 40px auto;'>Your intelligent assistant for mastering tasks and optimizing sleep for peak performance.</p>", unsafe_allow_html=True)
    
    # Center the buttons
    cols = st.columns([1, 0.8, 1])
    with cols[1]:
        # REMOVED the unneeded <style> block that was here
        
        st.button("🎓 Student Mode", use_container_width=True, on_click=lambda: st.session_state.update(user_type="student"), key="student_mode_button")
        st.button("💼 Professional Mode", use_container_width=True, on_click=lambda: st.session_state.update(user_type="professional"), key="professional_mode_button")
        
        # This will trigger rerun correctly for the above on_click callbacks
        if "student_mode_button" in st.session_state and st.session_state["student_mode_button"]:
            st.rerun()
        if "professional_mode_button" in st.session_state and st.session_state["professional_mode_button"]:
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --- 2. TASKS PAGE ---

def render_tasks_page():
    """Renders the main task management interface."""
    st.markdown("## ✅ Task Manager")
    st.markdown("<p>Organize, prioritize, and conquer your to-do list.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Use an expander to hide the form when not needed
        with st.expander("➕ Add a New Task", expanded=True):
            with st.form(key="add_task_form"):
                task_title = st.text_input("Task Title", placeholder="e.g., Finalize project report")
                c1, c2 = st.columns(2)
                priority = c1.selectbox("Priority", ["High", "Medium", "Low"], index=1)
                due_date = c2.date_input("Due Date", date.today())
                
                if st.form_submit_button("Add Task", use_container_width=True, type="primary"):
                    if task_title:
                        add_task(task_title, priority.lower(), due_date)
                    else:
                        st.error("Please enter a task title.")

        st.markdown("<h3 style='margin-top: 20px;'>Your Task List</h3>", unsafe_allow_html=True)
        
        # Filter tabs
        filter_priority = st.radio("Filter by priority:", ["All", "High", "Medium", "Low"], horizontal=True, label_visibility="collapsed")
        
        tasks_to_show = st.session_state.tasks
        if filter_priority != "All":
            tasks_to_show = [t for t in st.session_state.tasks if t['priority'] == filter_priority.lower()]

        if not tasks_to_show:
            st.info("No tasks here. Add one above or select a different filter!")
        else:
            # Sort tasks: incomplete first, then by priority
            sorted_tasks = sorted(tasks_to_show, key=lambda x: (x['completed'], ['high', 'medium', 'low'].index(x['priority'])))
            
            for task in sorted_tasks:
                completed_class = "completed" if task['completed'] else ""
                priority_class = f"priority-{task['priority']}"
                
                st.markdown(f"<div class='task-item {completed_class}'>", unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns([0.15, 0.55, 0.2, 0.1])
                
                with c1:
                    # Use a unique key for the checkbox
                    st.checkbox("", task['completed'], key=f"check_{task['id']}", label_visibility="collapsed", on_change=toggle_task, args=(task['id'],))
                with c2:
                    synced_icon = "✓ Synced" if task['synced'] else ""
                    st.markdown(f"<div class='task-item-content'><div class='title'>{task['title']}</div><div class='details'>Due: {task['due_date']} {synced_icon}</div></div>", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"<span class='priority-badge {priority_class}'>{task['priority'].capitalize()}</span>", unsafe_allow_html=True)
                with c4:
                    # Use a unique key for the delete button
                    if st.button("🗑️", key=f"del_{task['id']}", help="Delete Task", on_click=delete_task, args=(task['id'],)):
                        st.rerun() # Rerun to reflect deletion immediately
                st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Overview")
        total, completed = len(st.session_state.tasks), sum(1 for t in st.session_state.tasks if t['completed'])
        
        st.markdown("<div class='card metric-card'>", unsafe_allow_html=True)
        progress = (completed / total * 100) if total > 0 else 0
        st.markdown(f"<div class='label'>COMPLETION RATE</div><div class='value'>{int(progress)}%</div>", unsafe_allow_html=True)
        st.progress(int(progress))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h5 style='margin-bottom: 15px;'>Pending Tasks by Priority</h5>", unsafe_allow_html=True)
        pending_tasks = [t for t in st.session_state.tasks if not t['completed']]
        st.metric("High Priority", sum(1 for t in pending_tasks if t['priority'] == 'high'))
        st.metric("Medium Priority", sum(1 for t in pending_tasks if t['priority'] == 'medium'))
        st.metric("Low Priority", sum(1 for t in pending_tasks if t['priority'] == 'low'))
        st.markdown("</div>", unsafe_allow_html=True)

# --- 3. SLEEP PAGE ---

def render_sleep_page():
    """Renders the sleep tracking interface."""
    st.markdown("## 🌙 Sleep Schedule")
    st.markdown("<p>Track your sleep to unlock peak energy and focus.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("### Log Your Sleep")
        with st.form("sleep_form", border=False):
            # Put the form inside a card
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            sleep_date = st.date_input("Date", date.today())
            c1, c2 = st.columns(2)
            bedtime = c1.time_input("Bedtime", datetime.strptime("22:30", "%H:%M").time())
            waketime = c2.time_input("Wake Time", datetime.strptime("06:30", "%H:%M").time())
            
            # Calculate and display duration inside the form
            duration = calculate_duration(bedtime.strftime("%H:%M"), waketime.strftime("%H:%M"))
            quality, color = get_sleep_quality(duration)
            
            st.markdown(f"""
            <div style='background: #F8F9FA; border-radius: 10px; padding: 20px; text-align: center; margin-top: 10px;'>
                <div style='font-size: 14px; color: #64748B;'>CALCULATED DURATION</div>
                <div style='font-size: 2.5em; font-weight: 700; color: {color}; margin: 5px 0;'>{duration} hours</div>
                <div style='font-size: 16px; font-weight: 600; color: {color};'>{quality} Quality</div>
            </div>
            """, unsafe_allow_html=True)

            if st.form_submit_button("Save Sleep Entry", use_container_width=True, type="primary"):
                add_sleep_entry(sleep_date, bedtime.strftime("%H:%M"), waketime.strftime("%H:%M"), duration)
            
            st.markdown("</div>", unsafe_allow_html=True)

        # Smart Suggestions
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h5 style='margin-bottom: 15px;'>💡 Smart Suggestions</h5>", unsafe_allow_html=True)
        for suggestion in get_smart_suggestions():
            st.markdown(f"<p style='font-size: 14px; margin: 8px 0;'>• {suggestion}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Recent History")
        if not st.session_state.sleep_data:
            st.info("No sleep data yet. Log your first night's sleep!")
        else:
            # Sort by date, newest first
            for entry in sorted(st.session_state.sleep_data, key=lambda x: x['date'], reverse=True)[:5]:
                quality, color = get_sleep_quality(entry['duration'])
                st.markdown(f"""
                <div class='card'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div>
                            <div style='font-weight: 600; font-size: 16px;'>{entry['date']}</div>
                            <div style='font-size: 13px; color: #64748B; margin-top: 5px;'>{entry['bedtime']} → {entry['waketime']}</div>
                        </div>
                        <div style='text-align: right;'>
                            <div style='font-size: 1.8em; font-weight: 700;'>{entry['duration']}h</div>
                            <div style='font-weight: 600; color: {color};'>{quality}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --- 4. ANALYTICS PAGE ---

def render_analytics_page():
    """Renders the charts and analytics dashboard."""
    st.markdown("## 📊 Analytics Dashboard")
    st.markdown("<p>Visualize your productivity and well-being trends.</p>", unsafe_allow_html=True)

    # Burnout Risk Assessment (move to top)
    risk, color = calculate_burnout_risk()
    st.markdown(f"""
    <div class='card' style='text-align: center; border-left: 5px solid {color};'>
        <div class='label'>BURNOUT RISK ASSESSMENT</div>
        <div class='value' style='color: {color}; font-size: 2.8em;'>{risk}</div>
        <p style='margin-top: 10px;'>Based on your recent sleep patterns and task workload.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Task Completion")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if st.session_state.tasks:
            completed = sum(1 for t in st.session_state.tasks if t['completed'])
            pending = len(st.session_state.tasks) - completed
            
            fig = go.Figure(data=[go.Pie(
                labels=['Completed', 'Pending'], 
                values=[completed, pending], 
                hole=.6,
                marker_colors=['#10B981', '#E2E8F0']
            )])
            fig.update_layout(height=350, showlegend=False, margin=dict(t=10, b=10, l=10, r=10),
                              annotations=[dict(text=f'<b>{completed}</b><br>Done', x=0.5, y=0.5, font_size=20, showarrow=False)])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No task data available to analyze.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Sleep Duration Trend")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if len(st.session_state.sleep_data) > 1:
            df = pd.DataFrame(st.session_state.sleep_data).sort_values('date')
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['duration'], 
                mode='lines+markers', name='Sleep',
                line=dict(color='#6366F1', width=3),
                marker=dict(size=8)
            ))
            # Add target lines
            fig.add_hline(y=7, line_dash="dash", line_color="#F59E0B", annotation_text="Minimum Target")
            fig.add_hline(y=9, line_dash="dash", line_color="#F59E0B", annotation_text="Maximum Target")
            
            fig.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), yaxis_title="Hours")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Log at least two nights to see a trend.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. BILLING PAGE (Professional Only) ---

def render_billing_page():
    """Renders the billing and time tracking page."""
    st.markdown("## 💰 Billing & Time Tracking")
    st.markdown("<p>Estimate earnings based on your completed tasks.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.session_state.hourly_rate = st.number_input("Your Hourly Rate (USD)", value=st.session_state.hourly_rate, min_value=1, step=5)
    
    # Simple estimation: assuming 1.5 hours per task for this demo
    hours_tracked = sum(1.5 for t in st.session_state.tasks if t['completed'])
    estimated_earnings = hours_tracked * st.session_state.hourly_rate
    
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Estimated Earnings")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card metric-card'><div class='label'>Completed Tasks</div><div class='value'>{}</div></div>".format(
            sum(1 for t in st.session_state.tasks if t['completed'])
        ), unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card metric-card'><div class='label'>Estimated Hours</div><div class='value'>{:.1f}h</div></div>".format(
            hours_tracked
        ), unsafe_allow_html=True)
    with col3:
        st.markdown("<div classs='card metric-card'><div class='label'>Est. Earnings</div><div class='value'>${:,.2f}</div></div>".format(
            estimated_earnings
        ), unsafe_allow_html=True)
    
    if st.button("Generate Invoice", type="primary"):
        st.success(f"Invoice for ${estimated_earnings:,.2f} generated successfully!")


# --- MAIN APP LOGIC ---

# 1. Check for user type. If None, show welcome page.
if st.session_state.user_type is None:
    render_welcome_page()
    st.stop() # Stop execution until user type is selected

# 2. Setup Sidebar (now that user type is known)
with st.sidebar:
    st.markdown(f"<h2 style='margin-bottom: 0;'>Planning Pro</h2><p>Mode: {st.session_state.user_type.capitalize()}</p>", unsafe_allow_html=True)
    
    # Define menu options based on user type
    menu_options = ["Tasks", "Sleep", "Analytics"]
    if st.session_state.user_type == "professional":
        menu_options.extend(["Team", "Billing"])
    
    # Use a clean radio button for navigation
    selected_tab = st.radio(
        "Navigation",
        menu_options,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Integrations")
    
    if st.session_state.google_connected:
        st.success("✓ Google Calendar Connected")
        if st.button("Sync Tasks", use_container_width=True):
            for task in st.session_state.tasks: task['synced'] = True
            st.toast("Tasks synced to Google Calendar!", icon="🔄")
    else:
        if st.button("Connect Google Calendar", use_container_width=True):
            st.session_state.google_connected = True
            st.rerun() # Rerun to show "Connected" status
    
    # Add a spacer and the "Switch Mode" button at the bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Switch Mode", use_container_width=True):
        st.session_state.user_type = None
        st.rerun()

# 3. Render the selected page
if selected_tab == "Tasks":
    render_tasks_page()
elif selected_tab == "Sleep":
    render_sleep_page()
elif selected_tab == "Analytics":
    render_analytics_page()
elif selected_tab == "Team":

    st.markdown("## 👥 Team Dashboard")
    st.info("Team features are coming soon in a future update!")
elif selected_tab == "Billing":
    render_billing_page()


