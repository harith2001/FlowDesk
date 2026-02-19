# FlowDesk – Multi-Tenant Business Management Platform

FlowDesk is a **multi-tenant business management platform** built with **Django, Django REST Framework, JWT auth, Celery, Redis, Channels, and React**.

It is designed as a **portfolio-grade mini SaaS** that showcases:

- Multi-tenant architecture with organization-based data isolation  
- Role-based access control (Owner/Admin/Manager/Employee)  
- Project and task management  
- Invoice and billing with PDF generation  
- Real-time notifications via WebSockets  
- Analytics dashboard endpoints  
- Audit logging of changes  

## Tech Stack

- **Backend**: Django, Django REST Framework  
- **Auth**: JWT + role-based permissions  
- **Database**: PostgreSQL (SQLite for local dev by default)  
- **Cache / Broker**: Redis  
- **Background Tasks**: Celery  
- **Realtime**: Django Channels (WebSockets)  
- **Frontend**: React (separate SPA)  
- **Deployment**: Docker + Nginx  

## Local Development (Backend)

From the project root (`FlowDesk`):

```bash
python -m venv .venv
# On Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

By default the backend uses **SQLite** for easy local setup, but `config/settings.py` includes a PostgreSQL-ready configuration you can switch to with environment variables.

## High-Level Backend Structure

Planned Django apps:

- `core/` – shared base models, mixins, utilities  
- `accounts/` – custom user model, authentication, JWT integration  
- `organizations/` – organizations, memberships, multi-tenant middleware  
- `projects/` – projects within an organization  
- `tasks/` – tasks, workflow, comments, attachments  
- `billing/` – invoices, invoice items, PDF generation via Celery  
- `notifications/` – notification model + Channels/WebSockets integration  
- `analytics/` – read-only analytics endpoints (revenue, productivity, etc.)  
- `audit/` – audit logging of CRUD changes  

The API is exposed under `/api/v1/` with **OpenAPI/Swagger docs** via `drf-spectacular`.

