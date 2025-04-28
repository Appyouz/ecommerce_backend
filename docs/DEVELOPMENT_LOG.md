# Development Log - E-commerce Project

## 2025-04-29 00:21 AM - Postgresql Setup & Initial User Authentication

-   **General:** Started working on setting up the database and implementing initial
    user authentication today. Focus was on getting the foundational backend pieces
    ready.

-   **Backend:**
    * Installed core backend packages: `django`, `djangorestframework`,
        `crispy-django-forms`, `bootstrap4-crispy`. (Note: Forgot to add `crispy_forms`
        to `INSTALLED_APPS` initially, leading to a problem later – fixed by adding
        it to `settings.py`).
    * Created main Django project (`ecommerce_backend`) and an app (`accounts`).
    * **PostgreSQL Setup:** This took some time to figure out, but it became
        straightforward once I understood the key steps for local setup on Arch Linux.
        * Initialized the database cluster (`initdb`).
        * Started and enabled the PostgreSQL service.
        * Learned how to access `psql` via the `postgres` user. Queries for
            creating a database, user, setting password, and granting privileges were
            similar enough to MySQL that it was easy to pick up.
        * *Problem:* Couldn't connect using a password from my normal user or Django
            initially. *Solution:* Discovered the need to configure `pg_hba.conf` to
            allow `md5` password authentication for local connections (`127.0.0.1/32` and
            `::1/128`). Edited the file and restarted the service. This fixed the
            connection issue.
        * Successfully tested connection using `psql -U <username> -d <dbname> -h 127.0.0.1`.
        * **Learning:** PostgreSQL setup involves more manual configuration steps
            compared to just installing MySQL, especially for authentication methods,
            but the core database interaction commands are quite similar. Need to
            research production setup differences later.
    * **User Authentication (Initial):**
        * **Decision:** For this MVP and as a beginner, decided to use Django's
            built-in user authentication system (`django.contrib.auth`). It handles
            most standard cases (login, signup, logout) out-of-the-box and is
            expandable if custom authentication is needed in the future. This is
            sufficient for the current use case.
        * Implemented basic login, signup, and logout views using Django's auth
            forms/views (no DRF API endpoints yet for auth).
        * Created basic HTML pages (`index.html`, `login.html`, `signup.html`) and
            a base template using Bootstrap 4 via `crispy-forms`.
    * Configured database settings in `settings.py` to point to the new
        PostgreSQL DB.

-   **Frontend:** No frontend work done yet for these features.
