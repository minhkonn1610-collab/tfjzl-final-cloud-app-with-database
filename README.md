# Online Course — Fresh Assessment Project

Clean Django project for the Coursera/IBM Online Course assessment assignment. This package is a new standalone codebase; it does not depend on personal GitHub accounts or their repositories.

## Requirements

- Python 3.10+
- pip

## Run locally (Windows PowerShell)

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py makemigrations onlinecourse
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for courses and `http://127.0.0.1:8000/admin/` to create courses, lessons, questions, and choices. Configure each question's correct choice(s) in the admin interface.

## Assessment routes

- `course/<course_id>/`
- `course/<course_id>/exam/`
- `course/<course_id>/submit/`
- `course/<course_id>/submission/<submission_id>/result/`

The result URL is named `show_exam_result` and the submit view redirects to that same name. Choice selection supports multiple correct answers per question.

## Before submitting to Coursera

1. Create/use a repository under your own GitHub account and keep the exact repository URL required by the grader.
2. Review the assignment rubric and verify the files in this clean project match the expected starter structure before replacing your existing repository contents.
3. Keep your previously accepted evidence screenshots, including `03-admin-site.png`, unless you have confirmed the grader no longer requires them.
4. Do not commit local databases, credentials, or virtual environments.

This package is provided as a clean standalone scaffold based on the assignment's required online-course assessment flow. A fresh local database is created when you run migrations; it does not include the original starter repository's course data.
