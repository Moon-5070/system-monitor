# 🖥️ System Monitor Dashboard

A **Django-based system monitoring platform** that collects and visualizes real-time system metrics such as CPU, RAM, and network usage across multiple agents.

---

## 🚀 Features

- **Real-time Monitoring** – Displays live updates of CPU, memory, and network stats.
- **Multi-Agent Support** – Each connected device runs an `agent.py` that sends data to the central Django server.
- **Web Dashboard** – Built-in HTML dashboard (`dashboard.html`) for visualizing system performance.
- **Modular Design** – Clear separation between server (Django) and client (Agent) for scalability.

---

## 🏗️ Project Structure

FORBOOTCAMP/
├── agent/
│ └── agent.py # Collects local system data and sends to server
│
├── monitor/
│ ├── templates/monitor/
│ │ ├── index.html # Main page
│ │ └── dashboard.html # Real-time visualization dashboard
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── ...
│
├── system_monitor/
│ ├── settings.py # Django settings
│ ├── urls.py
│ └── wsgi.py
│
├── db.sqlite3
├── manage.py
└── .gitignore


---

## ⚙️ Tech Stack

| Category | Technology |
|-----------|-------------|
| Backend | **Python (Django)** |
| Frontend | **HTML, JavaScript, Bootstrap** |
| Communication | **REST API, JSON** |
| Data | **SQLite3** |
| Monitoring | **psutil** (for system data collection) |

---

## 🧩 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Moon-5070/system-monitor.git
cd system-monitor

2️⃣ Set up Virtual Environment

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Run the Server

python manage.py runserver

