# Development Log - E-commerce Project
[ecommerce_frontend](https://github.com/Appyouz/ecommerce_frontend) 
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

## 2025-05-02 - Frontend Auth (Global State & Route Protection)

-   **General:** Focused on implementing global authentication state management
    and application-wide route protection on the frontend. This was a challenging
    day requiring significant use of external resources and examples, but resulted
    in the core authentication flow being managed globally across the application.

-   **Frontend:**
    * **Global Authentication State Management:** Implemented the `AuthContext`
        and `AuthProvider` using React Context API. This serves as a single source
        of truth for the user's authentication status (`isAuthenticated`), user
        data (`user`), and initial loading state (`isLoading`).
    * Used a `useEffect` within the `AuthProvider` to call the
        `WorkspaceAuthenticatedUser()` service function when the application loads.
        This checks for existing authentication (via HttpOnly cookies) and
        initializes the global state accordingly.
    * Provided the authentication state and the `loginSuccess` and
        `logoutSuccess` functions (which update the global state) via the
        `AuthContext.Provider`.
    * Created the `useAuth` custom hook for easily accessing the context state
        in components.
    * **Refactored Components for Global State:** Updated existing components:
    * `LoginForm.tsx`: Refactored to consume the `AuthContext` using `useAuth`.
        Removed local authentication checking state. The `handleSubmit` function
        now calls the `login` service and then calls `loginSuccess()` from the
        context to update the global state, triggering redirection via a `useEffect`
        that depends on the global state.
    * `Dashboard.tsx`: Refactored to consume the `AuthContext` using `useAuth`.
        Removed local user and loading states. This component now gets the user
        data, authentication status, and loading state directly from the global
        context.
    * **Implemented Application-Wide Route Protection:**
    * Added `useEffect` hooks in `LoginForm.tsx` and `Dashboard.tsx` that
        depend on the global `isLoading` and `isAuthenticated` state.
    * These effects correctly implement redirection logic: authenticated users
        landing on `/login` are redirected to `/dashboard`; unauthenticated users
        landing on `/dashboard` (after the initial check is complete) are
        redirected to `/login`.
    * **Display Authentication Status in UI (Globally):**
    * Created a shared `Header.tsx` component. This component consumes the
        global authentication state (`useAuth()`).
    * Implemented conditional rendering in the Header to show "Loading...",
        "Welcome, [Username]! Logout", or "Login / Sign Up" links based on
        the global `isLoading` and `isAuthenticated` state.
    * Included the Header component in the root `app/layout.tsx` within the
        `AuthProvider` to ensure it appears on all pages and has access to the
        global state.
    * Moved the primary logout button to the Header, ensuring it calls
        `logoutUser()` and `logoutSuccess()` from the context, followed by
        `router.push('/login')`.
    * **Logout Integration:** The logout action now primarily handled by the
        Header component correctly calls the `logoutUser` service function
        (which triggers backend cookie clearing) and then calls the `logoutSuccess()`
        function from the context to update the global state, causing the route
        protection `useEffect` to trigger redirection. (Note: A local logout
        button on Dashboard was also kept and updated).
    * Acknowledged that implementing the Dashboard component's logic and the global
        state pattern required significant referencing of external code examples due to
        their complexity and personal fatigue. Committed to revisiting this code to
        deepen understanding later.
    * Continued using and getting more comfortable with TypeScript as it helps clarify
        expected data shapes.

-   **Backend:** No backend code changes were strictly needed for implementing the
    global frontend state management today, confirming the backend authentication
    API and cookie setup from previous sessions were correctly completed and ready.

-   **Learning:** Gained practical experience implementing a standard global state
    management pattern using React Context API. Learned how to structure an
    `AuthProvider` and `useAuth` hook. Understood how to use `useEffect` in the
    provider for initial asynchronous state initialization. Learned how to refactor
    components to consume a global context. Successfully implemented robust
    client-side route protection logic that relies on global authentication state.
    Integrated API service calls (login, logout, fetch user) with global state
    updates. Reinforced that complex patterns often require learning from external
    resources and that understanding can deepen through review and use. Learned how
    to create and use shared UI components that depend on global application state.

---


## 2025-05-05 - Product Catalog Backend

-   **General:** Started working on the Product Catalog milestone today. Focused
    on building the core backend pieces for managing products and categories.

-   **Backend:**
    * Created the `Product` and `Category` models.
    * Created DRF `serializers` for both models to handle data conversion to/from JSON.
        Configured the `ProductSerializer` to nest the `CategorySerializer` for
        read operations, showing full category details instead of just the ID.
    * Created DRF `ViewSets` for `Product` and `Category`. Implemented list and
        retrieve views. Used `ModelViewSet` which provides these automatically.
    * Learned that I can make multiple commits locally before pushing them all
        at once to the remote repository.

-   **Learning:** Gained experience defining Django models with relationships.
    Learned how to create DRF `ModelSerializers` and use nested serializers for
    representing related data. Practiced using `ModelViewSet` for standard API
    endpoints like list and retrieve.

---

## 2025-05-06 - Product Detail Frontend

-   **General:** Worked on creating the frontend page for displaying individual
    product details today. It felt relatively straightforward.

-   **Frontend:**
    * Created the `ProductDetailPage` component.
    * The main challenge was handling the passing of the product `id` as a
        parameter for routing. Initially tried using props which didn't work
        for this, then used `useParams` (from a React Router context, likely
        needed to figure out Next.js's way for this), which worked, but I want
        to revisit this to ensure it's the correct Next.js App Router method
        later.
    * The coding logic for fetching and displaying the data was fairly simple
        once the parameter passing was figured out.

-   **Learning:** Gained initial experience with client-side routing and how to
    extract parameters from the URL to fetch data for a specific item. Realized
    the importance of understanding the specific routing method used by the
    framework (Next.js App Router in this case).

---

## 2025-05-07 - Frontend Restructure & Shopping Cart Backend

-   **General:** Started tackling features related to the Shopping Cart
    (Milestone 3 according to the plan). This involved some necessary frontend
    restructuring and significant backend work on the core cart logic.

-   **Frontend:**
    * Implemented a button on the product list view that navigates to the
        product detail page. Again faced a challenge with passing the product ID
        as a parameter specifically through the `onClick` event handler, requiring
        looking up how to do this correctly in React/JSX. The rest of the navigation
        logic felt intuitive.
    * **Restructured the project:** Decided to move components and project files
        out of the `src/app/` directory and place them directly under `src/`. The
        new structure under `src/` now includes `app/` (only for page routes),
        `context/`, `services/`, `ui/` (for components, planning to rename to `pages/`
        but unsure if this is the correct term for route components), and `type.ts`
        (for TypeScript definitions). Other library or feature components will be
        added to `src/` as needed.

-   **Backend:**
    * **Learning:** Gained practical experience in creating and configuring a new
        Django app (`cart`) specifically for the shopping cart feature, separating
        it from the `products` app. Learned how to move models between apps (if
        any were initially placed elsewhere) and update imports and migrations
        accordingly.
    * Implemented serializers for models with Foreign Key relationships and nested
        representations (`CartSerializer` including `CartItemSerializer`,
        `CartItemSerializer` including `ProductSerializer`).
    * Used `PrimaryKeyRelatedField` with `write_only=True` to handle foreign key
        assignment (like adding a product to a cart item) based on a provided ID
        in the incoming data.
    * Developed custom API views (`APIView`) and overrode `ModelViewSet` methods
        for specific logic related to the cart (e.g., adding/updating item quantity,
        filtering the queryset to show only the current user's cart, validating
        quantity on update).
    * Used `transaction.atomic` for database integrity during complex add/update
        operations involving multiple database changes.
    * Configured URLs for complex API structures using `DefaultRouter` and explicit
        `path` mappings to handle different cart actions.
    * Practiced testing authenticated API endpoints related to the cart using
        Insomnia/curl.
    * Debugged Django/DRF errors related to model managers, serializer Meta classes,
        and

---
