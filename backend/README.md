# 🛋️ Loafertools

> **An educational productivity tool designed to help students reduce procrastination and build consistent study habits.**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-NeonDB-blue?logo=postgresql&logoColor=white)

---

## 📖 Overview

Loafertools is a student-focused productivity platform that supports **structured focus sessions**, **tracks distractions**, and **encourages intentional breaks**. It helps students better manage their time, stay accountable, and improve overall academic productivity.

Built with simplicity, clarity, and practical habit formation in mind — no overwhelming features, just the essentials that work.

---

## ✨ Features

### 🎯 Focus Sessions
- **Pomodoro-style timer** with customizable duration (default: 25 minutes)
- Session types: `focus` or `break`
- Track start/end times and actual duration
- Mark sessions as completed

### 📋 Task Management
- Create tasks with titles, descriptions, and due dates
- **Priority levels** (1-5 scale) to organize what matters most
- Estimate required pomodoros per task
- Track completed pomodoros against estimates
- Break down tasks with **subtasks** for better organization

### 🚨 Distraction Tracking
- Log distractions during focus sessions
- Record distraction name and duration
- Gain awareness of what pulls your attention away
- Linked to specific focus sessions for detailed analysis

### 🔥 Streak System
- Track your **current streak** and **longest streak**
- Monitor total focus minutes across all sessions
- Count total sessions completed
- Last activity date tracking to maintain accountability

### 📊 Study Session Analytics
- Daily summary of focus and break minutes
- Sessions completed per day
- Distraction count tracking
- **Productivity score** (0-100) to measure daily effectiveness

### 💭 Daily Reflections
- Log your **mood** and **energy level** (1-5 scale)
- Record daily accomplishments
- Note challenges faced
- Build self-awareness over time

### 📚 Resource Library
- Save study resources with titles and URLs
- Categorize by resource type
- Add personal notes
- Mark favorites for quick access

### 💬 AI Chat Support
- Chat interface for study assistance
- Message history organized by conversation sessions
- User and assistant message tracking

### 💡 Feedback System
- Submit bug reports, feature requests, or general feedback
- Rate your experience (1-5 scale)
- Help improve the platform

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI (Python 3.11+) |
| **Database** | PostgreSQL (NeonDB) |
| **ORM** | SQLModel (SQLAlchemy + Pydantic) |
| **Migrations** | Alembic |
| **Auth** | JWT-based authentication |
| **Frontend** | *(Coming soon)* |

---

## 📁 Project Structure

```
backend/
├── main.py                 # Application entry point
├── pyproject.toml          # Dependencies & project config
├── alembic/                # Database migrations
│   └── versions/           # Migration scripts
└── app/
    ├── api/                # API routes & dependencies
    │   └── v1/routers/     # Versioned endpoint routers
    ├── core/               # Config, JWT, security
    ├── db/                 # Database connection
    ├── models/             # SQLModel data models
    ├── schemas/            # Pydantic request/response schemas
    └── utils/              # Helper utilities
```

---

## 🗄️ Data Models

| Model | Purpose |
|-------|---------|
| `User` | User accounts with username, email, and password |
| `FocusSession` | Timed focus/break sessions |
| `Distraction` | Interruptions logged during focus |
| `Task` | To-do items with priority and pomodoro tracking |
| `Subtask` | Breakdown of larger tasks |
| `Streak` | Daily usage streaks and totals |
| `StudySession` | Daily aggregated study statistics |
| `Reflection` | Daily mood, energy, and notes |
| `Resource` | Saved study materials and links |
| `ChatMessage` | AI assistant conversation history |
| `Feedback` | User-submitted feedback |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL database (or NeonDB account)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/loafertools.git
   cd loafertools/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file with:
   DATABASE_URL=your_postgresql_connection_string
   SECRET_KEY=your_jwt_secret_key
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

7. **Access API docs**
   Open `http://localhost:8000/docs` for interactive Swagger documentation.

---

## 🎨 The Final Product

When complete, Loafertools will be a **web application** where students can:

1. **Sign up and log in** securely
2. **Start focus timers** and track work sessions
3. **Log distractions** to understand productivity blockers
4. **Manage tasks** with priorities, subtasks, and pomodoro estimates
5. **View streaks** and daily statistics to stay motivated
6. **Reflect daily** on mood, energy, and accomplishments
7. **Save resources** for quick access during study
8. **Chat with an AI assistant** for study help
9. **Provide feedback** to improve the platform

The goal is a **clean, distraction-free interface** that helps students build lasting study habits without complexity.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <em>Built for students, by students. 📚✨</em>
</p>
