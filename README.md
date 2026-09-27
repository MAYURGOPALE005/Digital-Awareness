# Digital Privacy Awareness for Community Organization

A modern digital privacy awareness website built for a College Community Engagement Project (CEP). The project educates community members about online safety, password security, phishing prevention, app permissions, social media privacy, and safe digital payment habits.

## Tech Stack

- Frontend: HTML5, CSS3, Vanilla JavaScript
- Backend: Python, Django, Django REST Framework
- Database: SQLite
- Styling direction: dark navy theme with cyan accents, glassmorphism cards, and subtle motion

## Project Features

- Home page with digital privacy awareness overview
- Learn page with educational content on key privacy topics
- Interactive 10-question privacy quiz
- Digital safety tips page
- Community awareness survey form
- About CEP page
- Dashboard for results and statistics
- REST APIs for survey and quiz data

## Project Structure

```text
Digital Awareness/
├── backend/
│   ├── api/
│   ├── config/
│   ├── manage.py
│   └── db.sqlite3
├── frontend/
│   ├── css/
│   ├── js/
│   ├── about.html
│   ├── dashboard.html
│   ├── index.html
│   ├── learn.html
│   ├── quiz.html
│   ├── survey.html
│   └── tips.html
├── .env.example
├── .gitignore
├── Digital-Privacy-Awareness-CEP-Website.md
├── README.md
├── requirements.txt
└──
```

## Setup Instructions

1. Navigate to the project root.
2. Create and activate a virtual environment if needed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a local environment file from `.env.example` if needed.
5. Run database migrations:

```bash
cd backend
python manage.py migrate
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Open the app in a browser:

- Home: http://127.0.0.1:8000/
- Learn: http://127.0.0.1:8000/learn/
- Quiz: http://127.0.0.1:8000/quiz/
- Survey: http://127.0.0.1:8000/survey/
- Dashboard: http://127.0.0.1:8000/dashboard/

## API Endpoints

- POST /api/survey/
- GET /api/survey/results/
- GET /api/quiz/
- POST /api/quiz/result/
- GET /api/quiz/statistics/

## Notes

- The frontend uses the Fetch API to communicate with the Django REST API.
- The app avoids collecting sensitive personal data as required by the project specification.
- All form submissions and quiz answers are validated before being stored.
