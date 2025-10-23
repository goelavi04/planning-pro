# 📚 Planning Pro - Smart Task & Sleep Management

> A comprehensive productivity application with task management, sleep tracking, team wellness monitoring, and billing features.

![Planning Pro](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

### Core Modules
- ✅ **Task Management** - Priority-based task tracking with Google Calendar sync
- 😴 **Sleep Dashboard** - Weekly sleep pattern analysis with quality scoring
- 📊 **Analytics** - Interactive charts and burnout risk assessment
- 👥 **Team Workload** (Professional) - Team wellness and productivity monitoring
- 💰 **Billing Tracker** (Professional) - Time tracking and earnings calculation

### Key Highlights
- 🎨 Beautiful gradient UI with smooth animations
- 📱 Fully responsive (works on mobile devices)
- 🔗 Google Calendar API integration
- 📈 Real-time data visualization with Plotly
- 🚨 Burnout risk detection based on sleep + workload
- 🎯 Separate user flows for Students and Professionals

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/planning-pro.git
   cd planning-pro
```

2. **Create virtual environment**
```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Run the app**
```bash
   streamlit run app.py
```

5. **Open in browser**
   - Local: `http://localhost:8501`
   - Network: `http://YOUR_IP:8501`

## 📦 Requirements
```txt
streamlit==1.29.0
pandas==2.1.3
plotly==5.18.0
google-auth==2.25.0
google-auth-oauthlib==1.2.0
google-api-python-client==2.110.0
```

## 🔧 Configuration

### Google Calendar Setup (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` and place in project root
6. Run app and click "Connect Google Calendar"

### Streamlit Configuration

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#667eea"
backgroundColor="#f9fafb"
secondaryBackgroundColor="#ffffff"
textColor="#1f2937"

[server]
headless = true
port = 8501
```

## 📱 Mobile Access

1. Get your computer's IP address
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`

2. Ensure phone and computer on same WiFi

3. Open on phone: `http://YOUR_IP:8501`

4. Add to home screen for app-like experience

## 🏗️ Project Structure