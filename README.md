# Planning Pro

A web-based productivity app I built to help people manage their daily tasks while keeping track of their sleep habits. The idea came from noticing how easily students and working professionals burn out when they lose track of either their workload or sleep schedule.

## What does it do?

Planning Pro helps you stay on top of your tasks and monitor your sleep patterns. It's split into two modes - one for students and one for professionals - because they have different needs.

The app gives you insights into your productivity and warns you if you're heading towards burnout based on how much sleep you're getting versus how many tasks you have piling up.

## Why I built this

Most task apps focus only on getting things done but ignore your wellbeing. I wanted to create something that balances productivity with health. The burnout detection feature came from personal experience - I've seen too many friends (including myself) crash after pulling multiple all-nighters during exam season or project deadlines.

## Student Mode

This mode keeps things simple and focused on academic life:

**Task Management**
- Add assignments, readings, projects with due dates
- Set priority levels (high/medium/low) 
- Mark tasks complete when done
- Color-coded urgency indicators

**Sleep Tracking**
- Log when you sleep and wake up
- See your sleep patterns over the week
- Get quality ratings (optimal/acceptable/poor/critical)
- Charts showing if you're getting enough rest

**Analytics**
- Visual breakdown of completed vs pending tasks
- Sleep trends over time
- Burnout risk meter that combines your workload and sleep data
- Tells you if you need to slow down or can handle more

The analytics part might sound fancy, but it's really just charts that make your data easier to understand. Instead of looking at numbers, you see graphs that show patterns you might miss otherwise.

## Professional Mode

This includes everything from Student Mode plus features for working professionals:

**Team Dashboard**
- See your team members' workload
- Check everyone's average sleep (anonymized of course)
- Identify who might be struggling or burning out
- Helps managers distribute work more fairly

Why this matters: In most workplaces, managers don't know if someone's drowning in work until they burn out or quit. This gives early warnings.

**Billing Tracker**
- Set your hourly rate
- Track time spent on each task
- Calculate earnings automatically
- Generate quick invoice summaries

This is super useful for freelancers or anyone who bills clients by the hour. Instead of using a separate time tracking app, you track time while managing your tasks.

**What "Billing" actually means:**
It's basically a timer that runs when you work on tasks. Say you're a freelance designer charging $50/hour. You add a task "Design logo for Client X", work on it for 3 hours, and the app calculates that's $150 billable. At month-end, you can generate an invoice showing all tasks and total earnings.

**What "Analytics" means:**
Just a fancy word for turning your data into visual charts. Instead of seeing "Task 1: incomplete, Task 2: complete", you get a pie chart showing 60% of your tasks are done. Makes it way easier to see the big picture.

## Why Streamlit?

I chose Streamlit for a few practical reasons:

1. **Speed** - I could build this in Python without messing with HTML, CSS, and JavaScript separately. Everything's in one file.

2. **Data handling** - Since this app works with pandas DataFrames for sleep data and task lists, Streamlit made it natural to display that data.

3. **Charts** - Streamlit integrates perfectly with Plotly, which is what I used for all the graphs. Writing the code for interactive charts was surprisingly easy.

4. **No backend complexity** - For a college project, I didn't want to deal with setting up a separate backend server, database connections, API endpoints, etc. Streamlit handles all that.

5. **Fast iterations** - Every time I saved my code, the app reloaded automatically. Made testing new features really quick.

The downside? It's not great for very large apps or when you need complex user authentication. But for this project, it was perfect.

## Tech Stack

- **Python** - Main language
- **Streamlit** - Web framework
- **Pandas** - Data management
- **Plotly** - Interactive charts
- **Google Calendar API** - Task syncing (optional)

## How to run it locally

```bash
# Clone the repo
git clone https://github.com/yourusername/planning-pro.git
cd planning-pro

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## Using it on your phone

If you want to use this on your phone while your laptop's running the app:

1. Make sure your phone and laptop are on the same WiFi
2. Find your laptop's IP address (run `ipconfig` on Windows or `ifconfig` on Mac)
3. On your phone's browser, go to `http://YOUR_IP:8501`
4. Add it to your home screen for quick access

## Features I'm proud of

**Burnout Detection Algorithm**
This combines your sleep average with your pending high-priority tasks. If you're sleeping less than 6 hours consistently AND have more than 5 urgent tasks, it flags you as "Critical Risk". The thresholds were based on research about optimal sleep duration and cognitive load.

**Real-time Updates**
Everything updates instantly. Mark a task complete, and your stats refresh immediately. Log your sleep, and the chart updates right away. No page reloads needed.

**Mobile Responsive**
Works just as well on phones as on laptops. I tested it on my iPhone throughout development.

## What I learned

Building this taught me:
- How to structure a full-stack app (even though Streamlit handles most of it)
- Working with dates and times is annoying (sleep duration calculation was tricky when crossing midnight)
- User experience matters more than features (I removed several "cool" features because they made the app confusing)
- Data visualization is powerful (charts make patterns obvious that raw numbers hide)

## Limitations

**No database** - Right now, data resets when you close the app. I kept it simple for the project, but a real version would need PostgreSQL or MongoDB.

**No authentication** - Anyone who opens the app can see everything. Not great for actual team use.

**Google Calendar sync is simulated** - Getting real OAuth working and deploying it publicly was too complex for the deadline. It works locally if you set up credentials, but the deployed version just shows a mock connection.

## Future improvements

If I continue this:
- Add persistent storage (probably PostgreSQL)
- User accounts and authentication
- Email reminders for upcoming deadlines
- Integration with Fitbit/Apple Health for automatic sleep tracking
- Dark mode (because why not)
- AI suggestions based on your patterns

## Why this project matters

Everyone talks about productivity, but not enough people talk about sustainable productivity. You can't just keep adding tasks to your plate without considering your capacity. This app tries to be the voice that says "hey, you need to sleep" when you're pushing too hard.

For teams, it helps managers see when someone's struggling before it becomes a crisis. That's genuinely useful in preventing burnout in workplace environments.

## Running it yourself

Everything you need is in the repo. The code's commented where it might be confusing. If you want to add features or modify it, the app.py file is organized into clear sections for each module.

## Project context

Built this for my college project course. Required demonstrating two modules working - I chose Task Management and Sleep Dashboard as the core ones, then added Team and Billing features for the Professional mode to make it more comprehensive.

The professor wanted to see practical applications of Python, data visualization, and web development. This covers all three.

---

**Note**: This is an academic project. While it works and I use it myself, it's not production-ready without adding proper authentication, database, and security measures.