# MedIntern - Hospital Internship Platform

MedIntern is a comprehensive web application designed to manage the entire lifecycle of medical internships. It connects three key stakeholders: **Medical Students**, **Hospitals**, and **Faculty/University Administration**.

The platform facilitates internship offer creation, student applications, placement tracking, daily journaling, and evaluations.

## 🚀 Getting Started

### Prerequisites
- **Python** (3.8+)
- **Node.js** (16+)
- **Git**

### 1. Backend Setup (Django)

The backend is a Django REST Framework application.

```bash
# Navigate to backend directory
cd GP/backend

# Create a virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Configure Environment
Before running the backend, you must create your own private `.env`
file.

### 1. Enter the backend folder:

``` bash
cd mma/backend
```

### 2. Generate a unique Django SECRET_KEY:

``` bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key.

### 3. Create your `.env` file:

``` bash
# Windows (PowerShell)
cp .env.example .env
notepad .env

# Mac/Linux
cp .env.example .env
nano .env
```

Inside `.env`, paste your secret key:

``` env
SECRET_KEY=your_generated_secret_key_here
DEBUG=True
DB_ENGINE=sqlite  # Default for development
```

> **Note:** `.env` is ignored by Git --- the key stays safe.

------------------------------------------------------------------------

#  .env --- Recommended Development Structure

``` env
# Development settings
DEBUG=True

# Database - Choose ONE
DB_ENGINE=sqlite  # sqlite, mysql, or postgresql

# For MySQL/PostgreSQL only:
# DB_NAME=mma_db
# DB_USER=username
# DB_PASSWORD=password
# DB_HOST=localhost
# DB_PORT=3306

# Service settings (when running without Docker)
SERVICE_NAME=users-service  # Change per service
DJANGO_HOST=127.0.0.1
DJANGO_PORT=8001  # Change per service (8001, 8002, etc.)
CONSUL_HOST=localhost
RABBITMQ_HOST=localhost
```

------------------------------------------------------------------------

# Run Migrations
python manage.py migrate

# Create a Superuser (Admin) to manage the system
python manage.py createsuperuser

# Start the Server
python manage.py runserver
```
*Backend will run at `http://localhost:8000`*

### 2. Frontend Setup (Vue 3 + Vite)

The frontend is a Vue 3 application using Vite and Tailwind CSS.

```bash
# Open a new terminal and navigate to frontend directory
cd GP/frontend

# Install Dependencies
npm install

# Start the Development Server
npm run dev
```
*Frontend will run at `http://localhost:5173`*

---

## 👥 User Management & Roles

This application is an **internal platform**. Users are not created via public sign-up. They are strictly managed to ensure security and role integrity.

### How to Create Users
1.  **Initial Setup**: Log in to the **Django Admin Panel** (`http://localhost:8000/admin`) using the superuser account you created.
2.  **Create Users**: Go to the `Users` section.
3.  **Assign Roles**: specific roles define the user's dashboard and permissions:
    - `Student`: Must have a linked `StudentProfile` (Matricule, Level, Specialty).
    - `Hospital Admin`: Manages offers and staff for a specific hospital.
    - `Faculty Admin`: Validates offers and oversees all students.
    - `Encadrant` (Supervisor): Supervises assigned interns (doctors/professors).

### Demo Credentials (Development Only)
The login screen (`LoginView.vue`) contains a "Demo Accounts" section for quick testing:
- **Student**: Login with Matricule `123456789012`
- **Hospital Admin**: Login with Email `admin@example.com`

---

## 🔄 Core Workflows

### 1. Internship Offer Workflow
1.  **Creation**: **Hospital Admin** logs in → "Create Offer" → Fills details (Department, Level, Skills). Status: `Draft` -> `Pending`.
2.  **Validation**: **Faculty Admin** logs in → "Offers to Validate" → Reviews offer → Validates. Status: `Open`.
3.  **Visibility**: Offer becomes visible to students matching the level/specialty.

### 2. Application Process
1.  **Apply**: **Student** browses "Internships" → Selects Offer → Clicks "Apply".
2.  **Selection**: **Student** can prioritize applications (1st, 2nd, 3rd choice).
3.  **Review**: **Hospital Admin** views "Applications" → Accepts or Rejects the student.
4.  **Placement**: If Accepted, an `Internship` record is created (Status: `Pending Start`).

### 3. Active Internship Dynamics
1.  **Journaling**: **Student** logs daily activities in "Journal".
2.  **Supervision**: **Supervisor (Encadrant)** reviews journals and adds comments.
3.  **Scheduling**: Shifts and meetings are tracked in the "Calendar".
4.  **Evaluation**: At the end, **Supervisor** fills out an evaluation form for the student.

---

## 🛠️ Verification & Monitoring

### How to check if everything is going well

1.  **System Status Check**:
    Run the generic system check built into Django:
    ```bash
    python manage.py check
    ```

2.  **Database & Data Integrity**:
    A custom script is provided to inspect the database state (offers, admins):
    ```bash
    python GP/backend/check_db.py
    ```
    *This script prints a summary of existing Internship Offers and Hospital Admins.*

3.  **Frontend Routes**:
    Navigate to `http://localhost:5173/`. If it redirects to `/login` (or `/dashboard` if logged in), the routing (Vue Router) and State Management (Pinia) are working.

4.  **API Connectivity**:
    The Frontend relies on the Backend running at port 8000. If you see "Network Error" or infinite loading spinners, ensure the backend terminal is running and no firewall is blocking `localhost:8000`.

### Key Commands Reference

| Action | Command (in respective dir) |
| :--- | :--- |
| **Run Backend** | `python manage.py runserver` |
| **Run Frontend** | `npm run dev` |
| **Make Migrations** | `python manage.py makemigrations` |
| **Apply DB Changes** | `python manage.py migrate` |
| **Create Admin** | `python manage.py createsuperuser` |
| **Build Frontend** | `npm run build` |
