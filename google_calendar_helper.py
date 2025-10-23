# ============================================
# FILE: google_calendar_helper.py
# Save this in your project folder
# ============================================

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Get authenticated Google Calendar service"""
    creds = None
    
    # Check if token exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("credentials.json not found! Get it from Google Cloud Console.")
            
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def sync_task_to_calendar(task):
    """Sync a single task to Google Calendar"""
    try:
        service = get_calendar_service()
        
        # Create event
        event = {
            'summary': f"[{task['priority'].upper()}] {task['title']}",
            'description': f"Priority: {task['priority']}\nStatus: {'Completed' if task['completed'] else 'Pending'}",
            'start': {
                'date': task['due_date'],
            },
            'end': {
                'date': task['due_date'],
            },
            'colorId': get_color_id(task['priority']),
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},
                ],
            },
        }
        
        # Insert event
        result = service.events().insert(calendarId='primary', body=event).execute()
        return True, result['id']
    
    except Exception as e:
        return False, str(e)

def get_color_id(priority):
    """Get Google Calendar color for priority"""
    colors = {
        'high': '11',    # Red
        'medium': '5',   # Yellow  
        'low': '2'       # Green
    }
    return colors.get(priority, '1')

def sync_all_tasks(tasks):
    """Sync multiple tasks to Google Calendar"""
    synced_count = 0
    errors = []
    
    for task in tasks:
        if not task.get('synced', False):
            success, result = sync_task_to_calendar(task)
            if success:
                task['synced'] = True
                task['calendar_event_id'] = result
                synced_count += 1
            else:
                errors.append(f"{task['title']}: {result}")
    
    return synced_count, errors

def list_upcoming_events(max_results=10):
    """List upcoming calendar events"""
    try:
        service = get_calendar_service()
        now = datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
    except Exception as e:
        return []

def delete_calendar_event(event_id):
    """Delete event from Google Calendar"""
    try:
        service = get_calendar_service()
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True
    except Exception as e:
        return False


# ============================================
# UPDATE YOUR app.py - ADD THIS SECTION
# ============================================

# Add this at the top of app.py after imports:
"""
try:
    from google_calendar_helper import sync_all_tasks, get_calendar_service
    GOOGLE_CAL_AVAILABLE = True
except ImportError:
    GOOGLE_CAL_AVAILABLE = False
"""

# Replace the Google Calendar button section in sidebar with:
"""
st.markdown("### 🔗 Google Calendar")

if GOOGLE_CAL_AVAILABLE:
    if st.session_state.google_connected:
        st.success("✅ Connected")
        if st.button("📤 Sync Tasks"):
            with st.spinner("Syncing to Google Calendar..."):
                synced_count, errors = sync_all_tasks(st.session_state.tasks)
                
                if synced_count > 0:
                    st.toast(f"✅ Synced {synced_count} tasks!", icon="✅")
                    st.rerun()
                
                if errors:
                    for error in errors:
                        st.error(error)
    else:
        if st.button("Connect Google"):
            with st.spinner("Connecting..."):
                try:
                    service = get_calendar_service()
                    st.session_state.google_connected = True
                    st.toast("✅ Connected to Google Calendar!", icon="✅")
                    st.rerun()
                except FileNotFoundError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")
else:
    st.warning("⚠️ Install: pip install google-auth google-auth-oauthlib google-api-python-client")
"""