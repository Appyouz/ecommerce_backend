# Development Log - E-commerce Project

## 2025-04-28 00:21 AM - Postgresql Setup & Initial User Authentication

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


## 2025-04-29 - PostgreSQL Fixes & Auth Libraries Setup

-   **General:** Focused on resolving lingering PostgreSQL setup issues and tackling
    the complex backend authentication library integration today. It was challenging
    but ultimately successful.

-   **Backend:**
    * Had trouble with PostgreSQL setup again due to forgetting the password,
        requiring a partial re-setup/uninstall process. Resolved the password issue.
    * Integrated PostgreSQL with the Django project using `django-environ`. This
        took about an hour, learning how to configure the database URL string in the
        `.env` file and use `env.db()`.
    * Used `django-environ` as it's new to me, specifically for Django, and helps
        keep configuration clean, separate from the codebase.
    * Also learned how to generate a random secret key using Django's utility
        function for better security in production.
    * *Problem:* Encountered a `MigrationSchemaMissing` error ("permission denied for
        schema public") when running `python manage.py migrate` after connecting to
        PostgreSQL with the new user.
    * *Solution:* The database user (`ecommerce_admin`) didn't have sufficient
        privileges on the default `public` schema to create tables. Had to grant
        `USAGE` and `CREATE` privileges on the `public` schema to the user and set
        the user as the owner of the database.
        ```bash
        GRANT USAGE, CREATE ON SCHEMA public TO ecommerce_admin;
        ALTER DATABASE ecommerce_db OWNER TO ecommerce_admin;
        ```
        Migrations ran successfully after this.
    * Tackled the integration of `djangorestframework-simplejwt`, `dj-rest-auth`,
        and `allauth`. This was the most challenging part ("horrible day," "lost for
        hours"). The documentation felt complicated, making it hard to know where to
        start and connect the pieces.
    * *Outcome of Struggle:* Successfully configured `settings.py` and project
        `urls.py` based on documentation and examples found.
        * Added `rest_framework`, `rest_framework.authtoken` (needed by some libs),
            `rest_framework_simplejwt`, `dj_rest_auth`, `dj_rest_auth.registration`,
            `allauth`, `allauth.account`, `allauth.socialaccount` to `INSTALLED_APPS`.
        * Added `allauth.account.middleware.AccountMiddleware` to `MIDDLEWARE`.
        * Configured `REST_FRAMEWORK` to use `JWTAuthentication` and
            `JWTCookieAuthentication` by default.
        * Set `REST_AUTH = {'USE_JWT': True}` and `SITE_ID = 1`.
        * Configured a console backend for emails (`EMAIL_BACKEND`), required by
            `allauth`.
        * Included URLs for `simplejwt` token views and `dj-rest-auth` core and
            registration views in `ecommerce_backend/urls.py` under API paths:
            ```python
            # ... other imports
            from rest_framework_simplejwt.views import (TokenObtainPairView,
                                                        TokenRefreshView)
            # ... urlpatterns start
                path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                path('dj-rest-auth/', include('dj_rest_auth.urls')),
                path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
            # ...
            ```
    * Tested the registration and login endpoints provided by `dj-rest-auth`
        using Insomnia.
        * **Registration (`POST /dj-rest-auth/registration/`):** Works with
            `username`, `email`, `password`, `password2` JSON body.
        * **Login (`POST /dj-rest-auth/login/`):** Works with `username`,
            `password` JSON body, successfully returns JWT access and refresh tokens.
    * Encountered a message on logout endpoint about cookies/blacklisting not
        enabled. Understand this means server-side token invalidation isn't configured
        and client needs to delete the token. (Decided to accept client-side deletion
        for MVP).
    * *Decision:* Keeping the old `accounts/` app with template views for now,
        though it's not part of the API auth flow. Will remove later once API auth
        is fully confirmed working with frontend.
    * **Learning:** Integrating multiple authentication libraries is complex and
        requires careful attention to documentation, settings, and URL inclusion.
        Debugging permission errors in PostgreSQL requires understanding database schemas.

-   **Frontend:**
    * Started the frontend project setup using `create-next-app`.
    * Made specific choices during setup: No TypeScript, Yes ESLint, No Tailwind CSS,
        Yes `src/` directory, Yes App Router, Yes Turbopack. These align with
        previous decisions to manage learning load and focus on core logic.
    * Frontend setup is complete.

---

