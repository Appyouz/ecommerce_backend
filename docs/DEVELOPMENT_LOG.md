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

## 2025-04-30 - Frontend Auth (Registration) & Next.js Setup

-   **General:** Focused on setting up the frontend project with Next.js and
    implementing the user registration form and API call. It was a challenging day
    filled with frustration and learning, ultimately resulting in a working
    registration process.

-   **Frontend:**
    * Reviewed React core concepts (components, props, state, hooks) via Next.js
        docs to refresh understanding before coding. Concepts feel clearer now, though
        still not an expert.
    * Started Next.js project setup (`ecommerce_frontend`) using `create-next-app`.
        Made choices: No TypeScript (initially!), Yes ESLint, No Tailwind CSS, Yes `src/`,
        Yes App Router, Yes Turbopack.
    * Figuring out the Next.js App Router structure (`src/app/`, `ui/`, `app/register/page.tsx`,
        `ui/register-form.tsx`) took time to understand how pages, layouts, and
        components link together. Used `ui/` directory for form components based on
        docs examples.
    * **Implemented the `RegisterForm` component:**
        * Used `useState` to manage form input data (`formData`), validation
            errors (`errors`), submission state (`isSubmitting`), overall submission
            error (`submitError`), and success state (`isSuccess`).
        * Created `handleChange` function to update `formData` state on input changes.
        * Implemented basic client-side validation within `handleSubmit` (checking
            required fields and password match).
        * Set up the `onSubmit` handler to prevent default form submission and manage
            `isSubmitting` state.
    * **Implemented the `registerUser` service function** (`services/auth.ts`).
        * This function handles the API call to the backend registration endpoint.
        * Used `Workspace` to make the `POST` request to the `dj-rest-auth` registration
            URL (`/dj-rest-auth/registration/`), setting appropriate headers
            (`Content-Type`, `Accept`) and sending the form data as a JSON string.
        * Included environment variable usage (`process.env.NEXT_PUBLIC_API_URL`) for
            the API base URL.
        * Included robust error handling: Checking `response.ok`, parsing the
            response body (JSON or text), and extracting/formatting error messages
            from the backend's response structure to throw a descriptive error if the
            API call fails. Handled network errors in the catch block.
    * **Unexpectedly adopted TypeScript:** While debugging errors and warnings (LSP
        help), found that adding type definitions (e.g., `FormData`, `FormErrors`,
        using `: React.ChangeEvent<HTMLInputElement>`) helped clarify expected data
        structures and resolve issues. Decided to embrace TypeScript and commit to
        learning it as part of this project's stack. It added another layer to the
        learning curve but seems beneficial.
    * **Key Challenges:** Figuring out the Next.js App Router structure and how to
        correctly initiate and handle the backend API call from the frontend component
        and service function were the biggest hurdles. Debugging CORS headers was
        also a point of focus (though mostly backend config changes were needed).
    * *Decision:* Incorporated basic client-side validation in the form for user
        experience, relying on backend for full validation.

-   **Backend:** No major backend code changes needed today, confirming the
    `dj-rest-auth` API setup from the previous session was correctly completed and
    ready to receive requests.

-   **Learning:** Gained practical understanding of React state and event handling
    for forms, the process of making asynchronous API calls from a frontend
    component using a service function, handling API responses and errors on the
    client side, and the basic structure of Next.js App Router. Also began the
    unexpected journey into learning TypeScript. Learned that figuring out complex
    integrations often requires looking at specific examples and adapting them,
    and that encountering and solving errors is a key way to learn new tools like
    TypeScript and understand library behaviors.

---

## 2025-05-01 - Frontend Auth (Login, Dashboard, Route Protection Attempt)
- **Started day by doing a crash document tutorial on typescript**

-   **General:** Focused on implementing the frontend login functionality, and
    starting on displaying user state and basic route protection. It was another
    day with significant challenges, requiring looking at resources and involving
    some necessary copying due to complexity and fatigue, but ultimately led to
    core features working.

-   **Frontend:**
    * **Login Form Implementation:** Created the `LoginForm` component and the
        corresponding `login` service function (`services/auth.ts`). Felt more
        straightforward than registration, building confidence in writing form and
        API calling logic mostly independently by adapting the registration code
        pattern.
    * Implemented `useState` for input fields, `isSubmitting`, `errors`, and added
        `isSuccess`/error state handling (felt good to implement these parts myself).
    * Updated `auth.ts` to include the `login` function (makes the POST request to
        the backend `/dj-rest-auth/login/` endpoint, handles response, checks
        `response.ok`, extracts errors). Also added `WorkspaceHomeData` (GET to `/`
        protected endpoint) and `logoutUser` (POST to `/dj-rest-auth/logout/`)
        service functions.
    * Used `credentials: 'include'` in `Workspace` calls for login, logout, and fetching
        protected data, necessary for sending/receiving HttpOnly cookies.
    * Implemented the `getCookie` helper function to retrieve the CSRF token from
        cookies and included the `X-CSRFToken` header in the `logoutUser` POST request,
        as required by Django's CSRF protection for cookie-based auth.
    * **Debugging JWT Cookie Visibility:** Figured out why JWT access tokens weren't
        appearing in standard browser headers or `document.cookie`. This was due to
        backend `SIMPLE_JWT` settings (`JWT_AUTH_COOKIE_HTTPONLY: True`) making them
        HttpOnly cookies, which are only visible in browser Developer Tools (Application/
        Storage tab) and automatically sent by the browser with requests. This involved
        tweaking several backend settings to ensure cookies were correctly issued.
    * **Dashboard Component & Initial Route Protection Attempt:** Created a basic
        `Dashboard` component. Used a `useEffect` to call `WorkspaceAuthenticatedUser()`
        on load to check authentication status.
        * If authenticated (`WorkspaceAuthenticatedUser()` returns user data), displays
            a welcome message and includes buttons to `WorkspaceHomeData` (to test access
            to a protected route) and `logoutUser`.
        * If not authenticated (`WorkspaceAuthenticatedUser()` returns null), redirects
            the user to the `/login` page.
    * Added a `useEffect` to the `LoginForm` component to perform a similar
        `WorkspaceAuthenticatedUser()` check on login page load and redirect authenticated
        users to `/dashboard`.
    * **Reflection on Dashboard/Protection Code:** Acknowledged that the implementation
        logic for the Dashboard component and the useEffects for route protection was
        largely copied due to fatigue and wanting to see the flow work. Committed
        to reviewing and fully understanding this code later. Realized this provides
        the desired flow: unauthenticated go to login, authenticated go to dashboard,
        login page redirects if already logged in.
    * Continued getting comfortable with TypeScript; can spot its usage and
        understand its purpose better now.

-   **Backend:**
    * Created the `accounts/serializers.py` file and implemented the `UserSerializer`
        to serialize user model data. This was my first time writing a DRF serializer
        from scratch.
    * Created `CustomLoginView` and `CustomLogoutView` in `accounts/views.py`,
        extending `dj_rest-auth` views.
        * `CustomLoginView` overrides `get_response` to include serialized user data
            in the login API response using the new `UserSerializer`.
        * `CustomLogoutView` is a basic pass-through (no override needed).
    * **Realization:** Discovered that the frontend is currently calling the default
        `dj-rest-auth` login/logout endpoints (at `/dj-rest-auth/login/`,
        `/dj-rest-auth/logout/`) due to URL configuration, and therefore my custom
        login/logout views (mapped at `/login/`, `/logout/`) are not currently being
        used by the frontend. Felt frustrating to spend time on unused code but
        understand *how* it works.
    * Noted the persistent `AUTHENTICATION_METHOD` deprecation warning but decided
        to ignore it for now as it doesn't break functionality.
    * Configured `REST_AUTH` and `SIMPLE_JWT` settings in `settings.py` to enable
        JWT HttpOnly cookies and token blacklisting (`ROTATE_REFRESH_TOKENS`,
        `BLACKLIST_AFTER_ROTATION`).

-   **Learning:** Solidified understanding of React state and event handling by
    implementing the login form. Learned to write a basic DRF serializer. Gained
    practical experience creating frontend service functions for API calls (login,
    logout, protected data fetch). Successfully implemented JWT HttpOnly cookie
    authentication from frontend to backend, including using `credentials: 'include'`
    and handling CSRF tokens for POST requests. Learned how to debug cookie behavior
    in browser dev tools. Began implementing client-side route protection patterns
    using `useEffect` and redirection based on authentication status checks. Learned
    that needing to copy complex logic when fatigued is okay, with the commitment
    to understand it later. Continued learning TypeScript through practice.

---

