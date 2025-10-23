import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Get authenticated Google Calendar service"""
    creds = None
    
    # Token file stores user's access tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def create_event(service, task):
    """Create calendar event from task"""
    event = {
        'summary': f"[{task['priority'].upper()}] {task['title']}",
        'description': f"Priority: {task['priority']}\nStatus: {'Completed' if task['completed'] else 'Pending'}",
        'start': {
            'date': str(task['due_date']),
        },
        'end': {
            'date': str(task['due_date']),
        },
        'colorId': get_color_id(task['priority'])
    }
    
    return service.events().insert(calendarId='primary', body=event).execute()

def get_color_id(priority):
    """Get Google Calendar color ID for priority"""
    colors = {
        'high': '11',    # Red
        'medium': '5',   # Yellow
        'low': '2'       # Green
    }
    return colors.get(priority, '1')

def sync_tasks_to_calendar(tasks):
    """Sync all tasks to Google Calendar"""
    try:
        service = get_calendar_service()
        synced = []
        
        for task in tasks:
            if not task.get('synced', False):
                event = create_event(service, task)
                task['synced'] = True
                task['event_id'] = event['id']
                synced.append(task)
        
        return True, len(synced), synced
    except Exception as e:
        return False, 0, str(e)

def list_upcoming_events(max_results=10):
    """List upcoming events from Google Calendar"""
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
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

def delete_event(event_id):
    """Delete event from Google Calendar"""
    try:
        service = get_calendar_service()
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True
    except Exception as e:
        return False