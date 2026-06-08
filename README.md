# NexoGrafix Backend

NexoGrafix Backend is a FastAPI-powered Content Management System (CMS) designed to handle website content, user management, newsletters, contact submissions, and media assets. It uses a combination of PostgreSQL for relational data and JSON files for dynamic content management.

## Features

- **JSON-based CMS:** Manage website content (Home, About, FAQs, etc.) through dynamic JSON files.
- **User Management:** Robust user and role-based access control.
- **Newsletter System:** Handle subscribers and newsletter distributions.
- **Contact & Feedback:** Manage contact requests and user feedback.
- **Media Management:** Support for image and video uploads.
- **Audit Logs:** Track system changes and user actions.
- **Health Monitoring:** Built-in health check endpoint.

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Language:** [Python 3.10+](https://www.python.org/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **Server:** [Uvicorn](https://www.uvicorn.org/)

## Project Structure

```text
├── app/
│   ├── api/            # API routes (v1)
│   ├── core/           # Configuration and security settings
│   ├── db/             # Database session and base model
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas for request/response
│   ├── seeders/        # Initial data seeders
│   ├── content/        # JSON files for website content
│   └── public/uploads/ # Uploaded media assets
├── main.py             # Application entry point
├── create_tables.py    # Script to initialize database tables
├── seed.py             # Script to seed initial data (roles, admin)
└── requirements.txt    # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd NexoGrafix_Backend
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the root directory and add your database connection string:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/nexografix_db
```

### Database Setup

1. **Create tables:**

   ```bash
   python create_tables.py
   ```

2. **Seed initial data:**

   ```bash
   python seed.py
   ```

## Running the Application

Start the development server using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

The API will be available at `http://localhost:8000`.

- **API Documentation (Swagger UI):** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`

## Deployment

This repository includes a GitHub Actions workflow that deploys the backend to a Hostinger KVM2 server over SSH.

### Required GitHub Secrets

- `HOSTINGER_HOST` - server IP or hostname
- `HOSTINGER_USER` - SSH username on the server
- `HOSTINGER_SSH_KEY` - private SSH key with access to the server
- `HOSTINGER_SSH_PORT` - SSH port, usually `22`
- `HOSTINGER_APP_DIR` - absolute path to the application directory on the server
- `HOSTINGER_SERVICE_NAME` - systemd service name used to restart the API process

### Server Requirements

- Python 3.10+ installed on the server
- A `venv`-based environment in the application directory
- A systemd service that starts the app with Uvicorn or Gunicorn
- A persistent `.env` file on the server with at least `DATABASE_URL` and `APP_URL`

The workflow syncs the repository contents to the server, installs Python dependencies, and restarts the service after a successful validation step.

## API Endpoints Overview

- `/api/v1/content`: Manage website sections via JSON.
- `/api/v1/users`: User management and authentication.
- `/api/v1/newsletter_subscribers`: Newsletter subscription management.
- `/api/v1/contact_submissions`: Manage contact form entries.
- `/api/v1/feedback`: User feedback collection.
- `/api/v1/stats`: Dashboard statistics.

## License

This project is proprietary. All rights reserved.
