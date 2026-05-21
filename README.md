DoubtStack – A Classroom Doubt Collector
<p align="center"> <img src="https://img.shields.io/badge/Django-5.x-green" /> <img src="https://img.shields.io/badge/Python-3.x-blue" /> <img src="https://img.shields.io/badge/TailwindCSS-Frontend-38B2AC" /> <img src="https://img.shields.io/badge/Database-SQLite3-orange" /> <img src="https://img.shields.io/badge/Status-Active-success" /> <img src="https://img.shields.io/badge/License-MIT-yellow" /> </p>
📌 Overview

DoubtStack – A Classroom Doubt Collector is a full-stack Django-based educational platform designed to improve classroom communication and streamline academic doubt management.

Traditional classrooms often face challenges such as hesitation in asking questions, repeated doubts, unstructured communication channels, and difficulty in tracking unresolved issues. DoubtStack addresses these limitations through a centralized digital platform where students can raise doubts and teachers can respond using multiple interactive methods.

The platform supports text-based discussions, audio replies, file uploads, multimedia explanations, whiteboard-based screen recordings, analytics dashboards, feedback systems, and a reusable department-level resource repository.

🎯 Objectives
Create a structured environment for doubt collection and resolution
Encourage participation through anonymous posting
Reduce repetitive questions using upvotes and shared resources
Improve communication between students and faculty
Provide data-driven insights using analytics
Build a permanent academic resource repository
Automate manual workflows
✨ Core Features
🔐 Authentication & User Management
Student login and registration
Teacher login and registration
Session-based authentication
OTP verification support
College database integration
Auto-fetch student/teacher details
Role handling:
Student
Teacher (Professor)
HOD
💬 Doubt Management
Submit doubts by subject/topic
Anonymous doubt posting
Unique doubt reference generation
Doubt status tracking:
Unresolved
Resolved
Escalated
Search and filtering
👍 Upvote System

Students can upvote doubts to indicate common concerns.

Features:

One vote per student
Dynamic vote counts
Prioritization of frequently asked doubts
💭 Interactive Reply System

Teachers can respond using:

Text
PDF/Documents
Audio
Video
Whiteboard recordings

Features:

Chat-style interface
Threaded discussions
Anonymous replies
File preview before upload
🖊️ Whiteboard Integration

Integrated Excalidraw iframe with screen recording support.

Capabilities:

Whiteboard drawing
Simultaneous screen + audio recording
Preview before upload
Upload using AJAX and MediaRecorder API
📚 Department Library

Teachers can bookmark important responses and save them permanently.

Features:

Subject-based filtering
Teacher-based filtering
File type filtering
Permanent resource repository
Responsive card layout
📊 Analytics Dashboard
Teacher Dashboard

Subject-wise analytics:

Total doubts
Resolution rate
Pending doubts
Feedback ratings
Doubt trends
HOD Dashboard

Department-wide analytics:

Total department doubts
Teacher performance
Subject activity
Resolution statistics
⭐ Feedback System

Students can rate:

Usefulness of replies
Clarity of explanations

Purpose:

Improve teaching quality
Measure response effectiveness
🔔 Notification System

Notifications for:

New doubt submission
New replies
Escalations
Feedback updates
Department library additions
⚙️ Automation Features

Using APScheduler:

Automatic Escalation

If:

status='unresolved'
created_at > 7 days

Action:

Escalate doubt to HOD
Automatic Cleanup

Every 14 days:

Delete old doubts
Delete replies
Delete votes
Remove orphan files

Exception:

Bookmarked resources remain permanently stored
🧱 System Architecture

The system follows Django's MVT (Model-View-Template) architecture.

Student / Teacher / HOD
            ↓
      Django Views
            ↓
Business Logic Layer
            ↓
 Django Models (ORM)
            ↓
       SQLite Database
            ↓
 Media Storage + APScheduler
🗂️ Project Structure
DoubtStack/
│
├── doubtstack/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── scheduler.py
│   └── utils.py
│
├── media/
│   ├── replies/
│   └── department_library/
│
├── static/
│
├── db.sqlite3
│
├── manage.py
│
└── requirements.txt
🧰 Technology Stack
Category	Technologies
Backend	Django 5.x, Python
Frontend	HTML, CSS, TailwindCSS, JavaScript
Database	SQLite3
Scheduler	APScheduler
Whiteboard	Excalidraw
Media Recording	MediaRecorder API
Icons	FontAwesome
Version Control	Git + GitHub
🚀 Installation

Clone repository:

git clone https://github.com/yourusername/DoubtStack.git

cd DoubtStack

Create virtual environment:

python -m venv venv

Activate environment:

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py makemigrations

python manage.py migrate

Run server:

python manage.py runserver

Open browser:

http://127.0.0.1:8000/
📈 Future Enhancements
AI-based similar doubt suggestion using NLP
AI-generated FAQ creation
WebSocket-based real-time updates
Advanced predictive analytics
LMS integration
Mobile application support
Recommendation engine for learning resources
📸 Screenshots

Add screenshots here:

Login Page
Student Dashboard
Teacher Dashboard
Chat Interface
Whiteboard Module
Department Library
Analytics Dashboard
🧪 Testing

Implemented test cases include:

✅ Authentication
✅ Doubt submission
✅ Anonymous posting
✅ Upvote system
✅ Multimedia replies
✅ Department library
✅ Feedback module
✅ Analytics dashboard
✅ Automatic escalation
✅ Automatic cleanup

👨‍💻 Contributors

Dani
MCA Project – DoubtStack: A Classroom Doubt Collector

📄 License

This project is licensed under the MIT License.

⭐ Support

If you found this project useful:

Star this repository
Fork it
Contribute improvements
Transforming classroom communication through structured digital learning.
