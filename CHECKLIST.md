# Django Project Checklist

Use this document as a practical, step-by-step reference when starting or maintaining a Django project. Adapt the app names, database, and deployment platform to the project requirements.

## 1. Plan the project

- [ ] Define the purpose of the application and its main user journeys.
- [ ] Identify the domain models, relationships, permissions, and external services.
- [ ] Decide whether the project needs a custom user model.
- [ ] Choose a supported Python and Django version.
- [ ] Decide which settings must come from environment variables.
- [ ] Choose a database for development and production.

## 2. Create an isolated Python environment

Create the environment in the project directory:

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Upgrade packaging tools and install Django:

```bash
python -m pip install --upgrade pip
python -m pip install django
```

Verify the installation:

```bash
python -m django --version
```

## 3. Create the project and applications

Create the Django project configuration:

```bash
django-admin startproject config .
```

Create focused applications for separate areas of functionality:

```bash
python manage.py startapp accounts
python manage.py startapp blog
```

Keep the project configuration separate from application code:

```text
project-root/
├── manage.py
├── config/
├── accounts/
├── blog/
├── templates/
├── static/
├── media/
├── requirements.txt
└── .env.example
```

## 4. Record dependencies and protect secrets

After installing project dependencies, create or update the dependency file:

```bash
python -m pip freeze > requirements.txt
```

Keep a safe example configuration in `.env.example`. Never commit real credentials:

```text
SECRET_KEY=replace-me
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
```

Add generated and sensitive files to `.gitignore`:

```text
.venv/
.env
__pycache__/
*.pyc
db.sqlite3
media/
staticfiles/
```

## 5. Configure settings

In `config/settings.py`:

- [ ] Add each local application to `INSTALLED_APPS`.
- [ ] Set `TEMPLATES[0]["DIRS"]` to include `BASE_DIR / "templates"`.
- [ ] Configure `STATIC_URL` and the source `STATICFILES_DIRS`.
- [ ] Configure `STATIC_ROOT` for collected production files.
- [ ] Configure `MEDIA_URL` and `MEDIA_ROOT` for uploads.
- [ ] Load secrets and environment-specific values from environment variables.
- [ ] Set `AUTH_USER_MODEL` before creating the first migration if using a custom user.
- [ ] Configure the database and email backend.
- [ ] Keep `DEBUG=True` only for local development.

Example static and media configuration:

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

## 6. Configure project URLs

In `config/urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Use named URL patterns and reverse them in Python and templates. Avoid hard-coded `.html` links.

## 7. Design models carefully

- [ ] Give every model a clear purpose and useful `__str__` method.
- [ ] Choose field types and constraints deliberately.
- [ ] Add `related_name` where reverse relationships will be used.
- [ ] Define `Meta.ordering` only when a default order is genuinely useful.
- [ ] Add database indexes or constraints for important query paths.
- [ ] Keep business rules in model methods or services, not templates.
- [ ] Avoid generating random values in a way that can create collisions.

Create and apply migrations after model changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

Review migration files before applying them to production.

## 8. Build forms and views

- [ ] Use `ModelForm` for model-backed forms.
- [ ] Validate user input in forms and enforce important constraints in models.
- [ ] Add CSRF protection to every state-changing form.
- [ ] Use `login_required` or explicit permission checks for protected views.
- [ ] Use `get_object_or_404` for detail pages.
- [ ] Redirect after successful POST requests (Post/Redirect/Get).
- [ ] Preserve submitted form data and show field-level errors after validation failures.
- [ ] Keep views small and readable; extract complex workflows into services.
- [ ] Use `select_related` and `prefetch_related` where they prevent N+1 queries.

## 9. Create templates and static assets

- [ ] Create a shared `templates/base.html`.
- [ ] Load static assets with `{% load static %}` and `{% static "..." %}`.
- [ ] Use template inheritance instead of duplicating page markup.
- [ ] Escape user-provided content by default.
- [ ] Add labels, helpful validation messages, and keyboard-friendly controls.
- [ ] Provide empty states for lists with no results.
- [ ] Add custom `404.html`, `403.html`, and `500.html` templates.
- [ ] Test layouts at mobile, tablet, and desktop widths.
- [ ] Check that text wraps correctly and no component causes horizontal overflow.

## 10. Configure authentication and administration

- [ ] Register models in `admin.py` with useful list displays and filters.
- [ ] Create a superuser for local administration:

  ```bash
  python manage.py createsuperuser
  ```

- [ ] Test registration, login, logout, password errors, and protected redirects.
- [ ] Confirm users cannot edit or delete objects they do not own.
- [ ] Configure password validation and secure session settings.
- [ ] If using a custom user model, verify admin forms and migrations carefully.

## 11. Add tests before calling the project complete

Test the behavior users depend on:

- [ ] Model creation, validation, constraints, and string representations.
- [ ] URL reversing and status codes.
- [ ] Anonymous and authenticated access.
- [ ] Form validation and invalid submissions.
- [ ] Successful POST redirects.
- [ ] Ownership and permission rules.
- [ ] Search, filtering, pagination, and empty states.
- [ ] Email generation using Django’s in-memory email backend.
- [ ] Custom error pages.

Run the checks and test suite:

```bash
python manage.py check
python manage.py test
```

Use a separate test database and avoid depending on local development data.

## 12. Check security settings

Before deployment:

- [ ] Set `DEBUG=False`.
- [ ] Set a strong, private `SECRET_KEY`.
- [ ] Configure `ALLOWED_HOSTS`.
- [ ] Configure `CSRF_TRUSTED_ORIGINS` when required.
- [ ] Use HTTPS in production.
- [ ] Set secure cookies and HSTS settings when HTTPS is active.
- [ ] Keep dependencies updated and scan for known vulnerabilities.
- [ ] Validate uploaded file types and sizes.
- [ ] Do not expose stack traces, secrets, or database files.

Run Django’s deployment checks:

```bash
python manage.py check --deploy
```

## 13. Prepare static files and deployment

Collect static assets:

```bash
python manage.py collectstatic
```

Production deployment should include:

- [ ] A production WSGI or ASGI server.
- [ ] A production database and backup strategy.
- [ ] Persistent media storage or a documented upload strategy.
- [ ] Environment variables configured outside source control.
- [ ] Migrations executed as part of the release process.
- [ ] Logging, monitoring, and health checks.
- [ ] A rollback plan.

Never use `runserver` as the production web server.

## 14. Final verification

- [ ] Start from a clean environment and install `requirements.txt`.
- [ ] Apply migrations successfully.
- [ ] Run `check` and `check --deploy`.
- [ ] Run all automated tests.
- [ ] Test the main user journeys manually.
- [ ] Test authentication and permission boundaries.
- [ ] Test forms with valid, invalid, missing, and unexpected input.
- [ ] Test mobile and desktop layouts.
- [ ] Confirm static files, media files, email, and error pages work.
- [ ] Review logs for warnings and unexpected errors.
- [ ] Document setup, environment variables, commands, and deployment steps in `README.md`.
