# Development Log - E-commerce Project
[ecommerce_frontend](https://github.com/Appyouz/ecommerce_frontend)
## 2025-04-28 00:21 AM - Postgresql Setup & Initial User Authentication

-   **General:** I started working on setting up the database and implementing
    initial user authentication today. My focus was on getting the foundational
    backend pieces ready.

-   **Backend:**
    * I installed core backend packages: `django`, `djangorestframework`,
        `crispy-django-forms`, `bootstrap4-crispy`. (Note to self: I initially
        forgot to add `crispy_forms` to `INSTALLED_APPS`, which caused a problem
        later, but I fixed it by adding it to `settings.py`).
    * I created my main Django project (`ecommerce_backend`) and an app (`accounts`).
    * **PostgreSQL Setup:** This part took some time to figure out, but it became
        straightforward once I understood the key steps for local setup on Arch Linux.
        * I initialized the database cluster (`initdb`).
        * I started and enabled the PostgreSQL service.
        * I learned how to access `psql` via the `postgres` user. The queries for
            creating a database, user, setting a password, and granting privileges
            were similar enough to MySQL that it was easy to pick up.
        * *Problem:* I couldn't connect using a password from my normal user or
            Django initially. *Solution:* I discovered the need to configure
            `pg_hba.conf` to allow `md5` password authentication for local connections
            (`127.0.0.1/32` and `::1/128`). After editing the file and restarting
            the service, this fixed the connection issue.
        * I successfully tested the connection using `psql -U <username> -d <dbname> -h 127.0.0.1`.
        * **Learning:** PostgreSQL setup involves more manual configuration steps
            compared to just installing MySQL, especially for authentication methods.
            However, the core database interaction commands are quite similar. I'll
            need to research production setup differences later.
    * **User Authentication (Initial):**
        * **Decision:** For this MVP and as a beginner, I decided to use Django's
            built-in user authentication system (`django.contrib.auth`). It handles
            most standard cases (login, signup, logout) out-of-the-box and is
            expandable if custom authentication is needed in the future. This is
            sufficient for the current use case.
        * I implemented basic login, signup, and logout views using Django's auth
            forms/views (I didn't use DRF API endpoints for auth yet).
        * I created basic HTML pages (`index.html`, `login.html`, `signup.html`) and
            a base template using Bootstrap 4 via `crispy-forms`.
    * I configured database settings in `settings.py` to point to the new
        PostgreSQL DB.

-   **Frontend:** No frontend work was done yet for these features.


## 2025-04-29 - PostgreSQL Fixes & Auth Libraries Setup

-   **General:** Today, I focused on resolving lingering PostgreSQL setup issues and
    tackling the complex backend authentication library integration. It was
    challenging but ultimately successful.

-   **Backend:**
    * I had trouble with PostgreSQL setup again due to forgetting the password,
        requiring a partial re-setup/uninstall process. I eventually resolved the
        password issue.
    * I integrated PostgreSQL with the Django project using `django-environ`. This
        took about an hour, as I learned how to configure the database URL string
        in the `.env` file and use `env.db()`.
    * I used `django-environ` because it was new to me, specifically for Django,
        and it helps keep configuration clean and separate from the codebase.
    * I also learned how to generate a random secret key using Django's utility
        function for better security in production.
    * *Problem:* I encountered a `MigrationSchemaMissing` error ("permission denied for
        schema public") when running `python manage.py migrate` after connecting to
        PostgreSQL with the new user.
    * *Solution:* The database user (`ecommerce_admin`) didn't have sufficient
        privileges on the default `public` schema to create tables. I had to grant
        `USAGE` and `CREATE` privileges on the `public` schema to the user and set
        the user as the owner of the database.
        ```bash
        GRANT USAGE, CREATE ON SCHEMA public TO ecommerce_admin;
        ALTER DATABASE ecommerce_db OWNER TO ecommerce_admin;
        ```
        Migrations ran successfully after this.
    * I tackled the integration of `djangorestframework-simplejwt`, `dj-rest-auth`,
        and `allauth`. This was the most challenging part (it felt like a "horrible
        day," and I was "lost for hours"). The documentation felt complicated, making
        it hard to know where to start and connect the pieces.
    * *Outcome of Struggle:* I successfully configured `settings.py` and project
        `urls.py` based on documentation and examples I found.
        * I added `rest_framework`, `rest_framework.authtoken` (needed by some libs),
            `rest_framework_simplejwt`, `dj_rest_auth`, `dj_rest_auth.registration`,
            `allauth`, `allauth.account`, `allauth.socialaccount` to `INSTALLED_APPS`.
        * I added `allauth.account.middleware.AccountMiddleware` to `MIDDLEWARE`.
        * I configured `REST_FRAMEWORK` to use `JWTAuthentication` and
            `JWTCookieAuthentication` by default.
        * I set `REST_AUTH = {'USE_JWT': True}` and `SITE_ID = 1`.
        * I configured a console backend for emails (`EMAIL_BACKEND`), which is
            required by `allauth`.
        * I included URLs for `simplejwt` token views and `dj-rest-auth` core and
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
    * I tested the registration and login endpoints provided by `dj-rest-auth`
        using Insomnia.
        * **Registration (`POST /dj-rest-auth/registration/`):** Worked with
            `username`, `email`, `password`, `password2` JSON body.
        * **Login (`POST /dj-rest-auth/login/`):** Worked with `username`,
            `password` JSON body, successfully returning JWT access and refresh tokens.
    * I encountered a message on the logout endpoint about cookies/blacklisting not
        enabled. I understood this means server-side token invalidation isn't
        configured, and the client needs to delete the token. (I decided to accept
        client-side deletion for the MVP).
    * *Decision:* I decided to keep the old `accounts/` app with template views for
        now, even though it's not part of the API auth flow. I'll remove it later
        once API auth is fully confirmed working with the frontend.
    * **Learning:** Integrating multiple authentication libraries is complex and
        requires careful attention to documentation, settings, and URL inclusion.
        Debugging permission errors in PostgreSQL requires understanding database
        schemas.

-   **Frontend:**
    * I started the frontend project setup using `create-next-app`.
    * I made specific choices during setup: No TypeScript, Yes ESLint, No Tailwind CSS,
        Yes `src/` directory, Yes App Router, Yes Turbopack. These choices aligned
        with my previous decisions to manage learning load and focus on core logic.
    * Frontend setup is complete.

---

## 2025-04-30 - Frontend Auth (Registration) & Next.js Setup

-   **General:** Today, I focused on setting up the frontend project with Next.js and
    implementing the user registration form and API call. It was a challenging day
    filled with frustration and learning, ultimately resulting in a working
    registration process.

-   **Frontend:**
    * I reviewed React core concepts (components, props, state, hooks) via Next.js
        docs to refresh my understanding before coding. Concepts feel clearer now,
        though I'm still not an expert.
    * I started the Next.js project setup (`ecommerce_frontend`) using
        `create-next-app`. I made choices: No TypeScript (initially!), Yes ESLint,
        No Tailwind CSS, Yes `src/`, Yes App Router, Yes Turbopack.
    * Figuring out the Next.js App Router structure (`src/app/`, `ui/`, `app/register/page.tsx`,
        `ui/register-form.tsx`) took time to understand how pages, layouts, and
        components link together. I used the `ui/` directory for form components
        based on documentation examples.
    * **Implemented the `RegisterForm` component:**
        * I used `useState` to manage form input data (`formData`), validation
            errors (`errors`), submission state (`isSubmitting`), overall submission
            error (`submitError`), and success state (`isSuccess`).
        * I created a `handleChange` function to update `formData` state on input changes.
        * I implemented basic client-side validation within `handleSubmit` (checking
            required fields and password match).
        * I set up the `onSubmit` handler to prevent default form submission and manage
            `isSubmitting` state.
    * **Implemented the `registerUser` service function** (`services/auth.ts`).
        * This function handles the API call to the backend registration endpoint.
        * I used `Workspace` to make the `POST` request to the `dj-rest-auth` registration
            URL (`/dj-rest-auth/registration/`), setting appropriate headers
            (`Content-Type`, `Accept`) and sending the form data as a JSON string.
        * I included environment variable usage (`process.env.NEXT_PUBLIC_API_URL`) for
            the API base URL.
        * I included robust error handling: checking `response.ok`, parsing the
            response body (JSON or text), and extracting/formatting error messages
            from the backend's response structure to throw a descriptive error if the
            API call fails. I handled network errors in the catch block.
    * **Unexpectedly adopted TypeScript:** While debugging errors and warnings (with
        LSP help), I found that adding type definitions (e.g., `FormData`, `FormErrors`,
        using `: React.ChangeEvent<HTMLInputElement>`) helped clarify expected data
        structures and resolve issues. I decided to embrace TypeScript and commit to
        learning it as part of this project's stack. It added another layer to the
        learning curve but seems beneficial.
    * **Key Challenges:** Figuring out the Next.js App Router structure and how to
        correctly initiate and handle the backend API call from the frontend component
        and service function were the biggest hurdles. Debugging CORS headers was
        also a point of focus (though mostly backend config changes were needed).
    * *Decision:* I incorporated basic client-side validation in the form for user
        experience, relying on the backend for full validation.

-   **Backend:** No major backend code changes were needed today, confirming the
    `dj-rest-auth` API setup from the previous session was correctly completed and
    ready to receive requests.

-   **Learning:** I gained practical understanding of React state and event handling
    for forms, the process of making asynchronous API calls from a frontend
    component using a service function, handling API responses and errors on the
    client side, and the basic structure of Next.js App Router. I also began the
    unexpected journey into learning TypeScript. I learned that figuring out complex
    integrations often requires looking at specific examples and adapting them,
    and that encountering and solving errors is a key way to learn new tools like
    TypeScript and understand library behaviors.

---

## 2025-05-01 - Frontend Auth (Login, Dashboard, Route Protection Attempt)
- **Started day by doing a crash document tutorial on TypeScript.**

-   **General:** Today, I focused on implementing the frontend login functionality, and
    starting on displaying user state and basic route protection. It was another
    day with significant challenges, requiring looking at resources and involving
    some necessary copying due to complexity and fatigue, but ultimately led to
    core features working.

-   **Frontend:**
    * **Login Form Implementation:** I created the `LoginForm` component and the
        corresponding `login` service function (`services/auth.ts`). This felt more
        straightforward than registration, building my confidence in writing form and
        API calling logic mostly independently by adapting the registration code
        pattern.
    * I implemented `useState` for input fields, `isSubmitting`, `errors`, and added
        `isSuccess`/error state handling (I felt good to implement these parts myself).
    * I updated `auth.ts` to include the `login` function (which makes the POST request to
        the backend `/dj-rest-auth/login/` endpoint, handles the response, checks
        `response.ok`, and extracts errors). I also added `WorkspaceAuthenticatedUser` (GET to `/`
        protected endpoint) and `logoutUser` (POST to `/dj-rest-auth/logout/`)
        service functions.
    * I used `credentials: 'include'` in `Workspace` calls for login, logout, and fetching
        protected data, which is necessary for sending/receiving HttpOnly cookies.
    * I implemented the `getCookie` helper function to retrieve the CSRF token from
        cookies and included the `X-CSRFToken` header in the `logoutUser` POST request,
        as required by Django's CSRF protection for cookie-based auth.
    * **Debugging JWT Cookie Visibility:** I figured out why JWT access tokens weren't
        appearing in standard browser headers or `document.cookie`. This was due to
        backend `SIMPLE_JWT` settings (`JWT_AUTH_COOKIE_HTTPONLY: True`) making them
        HttpOnly cookies, which are only visible in browser Developer Tools (Application/
        Storage tab) and automatically sent by the browser with requests. This involved
        tweaking several backend settings to ensure cookies were correctly issued.
    * **Dashboard Component & Initial Route Protection Attempt:** I created a basic
        `Dashboard` component. I used a `useEffect` to call `WorkspaceAuthenticatedUser()`
        on load to check authentication status.
        * If authenticated (`WorkspaceAuthenticatedUser()` returns user data), it displays
            a welcome message and includes buttons to `WorkspaceHomeData` (to test access
            to a protected route) and `logoutUser`.
        * If not authenticated (`WorkspaceAuthenticatedUser()` returns null), it redirects
            the user to the `/login` page.
    * I added a `useEffect` to the `LoginForm` component to perform a similar
        `WorkspaceAuthenticatedUser()` check on login page load and redirect authenticated
        users to `/dashboard`.
    * **Reflection on Dashboard/Protection Code:** I acknowledged that the implementation
        logic for the Dashboard component and the `useEffect`s for route protection was
        largely copied due to fatigue and and wanting to see the flow work. I committed
        to reviewing and fully understanding this code later. I realized this provides
        the desired flow: unauthenticated users go to login, authenticated users go to
        dashboard, and the login page redirects if already logged in.
    * I continued getting comfortable with TypeScript; I can spot its usage and
        understand its purpose better now.

-   **Backend:**
    * I created the `accounts/serializers.py` file and implemented the `UserSerializer`
        to serialize user model data. This was my first time writing a DRF serializer
        from scratch.
    * I created `CustomLoginView` and `CustomLogoutView` in `accounts/views.py`,
        extending `dj_rest-auth` views.
        * `CustomLoginView` overrides `get_response` to include serialized user data
            in the login API response using the new `UserSerializer`.
        * `CustomLogoutView` is a basic pass-through (no override needed).
    * **Realization:** I discovered that the frontend is currently calling the default
        `dj-rest-auth` login/logout endpoints (at `/dj-rest-auth/login/`,
        `/dj-rest-auth/logout/`) due to URL configuration. Therefore, my custom
        login/logout views (mapped at `/login/`, `/logout/`) are not currently being
        used by the frontend. It felt frustrating to spend time on unused code, but
        I understood *how* it works.
    * I noted the persistent `AUTHENTICATION_METHOD` deprecation warning but decided
        to ignore it for now as it doesn't break functionality.
    * I configured `REST_AUTH` and `SIMPLE_JWT` settings in `settings.py` to enable
        JWT HttpOnly cookies and token blacklisting (`ROTATE_REFRESH_TOKENS`,
        `BLACKLIST_AFTER_ROTATION`).

-   **Learning:** I solidified my understanding of React state and event handling by
    implementing the login form. I learned to write a basic DRF serializer. I gained
    practical experience creating frontend service functions for API calls (login,
    logout, protected data fetch). I successfully implemented JWT HttpOnly cookie
    authentication from frontend to backend, including using `credentials: 'include'`
    and handling CSRF tokens for POST requests. I learned how to debug cookie behavior
    in browser dev tools. I began implementing client-side route protection patterns
    using `useEffect` and redirection based on authentication status checks. I learned
    that needing to copy complex logic when fatigued is okay, with the commitment
    to understand it later. I continued learning TypeScript through practice.

---

## 2025-05-02 - Frontend Auth (Global State & Route Protection)

-   **General:** Today, I focused on implementing global authentication state management
    and application-wide route protection on the frontend. This was a challenging
    day requiring significant use of external resources and examples, but it resulted
    in the core authentication flow being managed globally across the application.

-   **Frontend:**
    * **Global Authentication State Management:** I implemented the `AuthContext`
        and `AuthProvider` using the React Context API. This serves as a single source
        of truth for the user's authentication status (`isAuthenticated`), user
        data (`user`), and initial loading state (`isLoading`).
    * I used a `useEffect` within the `AuthProvider` to call the
        `WorkspaceAuthenticatedUser()` service function when the application loads.
        This checks for existing authentication (via HttpOnly cookies) and
        initializes the global state accordingly.
    * I provided the authentication state and the `loginSuccess` and
        `logoutSuccess` functions (which update the global state) via the
        `AuthContext.Provider`.
    * I created the `useAuth` custom hook for easily accessing the context state
        in components.
    * **Refactored Components for Global State:** I updated existing components:
    * `LoginForm.tsx`: I refactored it to consume the `AuthContext` using `useAuth`.
        I removed local authentication checking state. The `handleSubmit` function
        now calls the `login` service and then calls `loginSuccess()` from the
        context to update the global state, triggering redirection via a `useEffect`
        that depends on the global state.
    * `Dashboard.tsx`: I refactored it to consume the `AuthContext` using `useAuth`.
        I removed local user and loading states. This component now gets the user
        data, authentication status, and loading state directly from the global
        context.
    * **Implemented Application-Wide Route Protection:**
    * I added `useEffect` hooks in `LoginForm.tsx` and `Dashboard.tsx` that
        depend on the global `isLoading` and `isAuthenticated` state.
    * These effects correctly implement redirection logic: authenticated users
        landing on `/login` are redirected to `/dashboard`; unauthenticated users
        landing on `/dashboard` (after the initial check is complete) are
        redirected to `/login`.
    * **Display Authentication Status in UI (Globally):**
    * I created a shared `Header.tsx` component. This component consumes the
        global authentication state (`useAuth()`).
    * I implemented conditional rendering in the Header to show "Loading...",
        "Welcome, [Username]! Logout", or "Login / Sign Up" links based on
        the global `isLoading` and `isAuthenticated` state.
    * I included the Header component in the root `app/layout.tsx` within the
        `AuthProvider` to ensure it appears on all pages and has access to the
        global state.
    * I moved the primary logout button to the Header, ensuring it calls
        `logoutUser()` and `logoutSuccess()` from the context, followed by
        `router.push('/login')`.
    * **Logout Integration:** The logout action is now primarily handled by the
        Header component. It correctly calls the `logoutUser` service function
        (which triggers backend cookie clearing) and then calls the `logoutSuccess()`
        function from the `AuthContext` to update the global state, causing the route
        protection `useEffect` to trigger redirection. (Note: A local logout
        button on Dashboard was also kept and updated).
    * I acknowledged that implementing the Dashboard component's logic and the global
        state pattern required significant referencing of external code examples due to
        their complexity and my personal fatigue. I committed to revisiting this code to
        deepen my understanding later.
    * I continued using and getting more comfortable with TypeScript as it helps clarify
        expected data shapes.

-   **Backend:** No backend code changes were strictly needed for implementing the
    global frontend state management today, confirming the backend authentication
    API and cookie setup from previous sessions were correctly completed and ready.

-   **Learning:** I gained practical experience implementing a standard global state
    management pattern using the React Context API. I learned how to structure an
    `AuthProvider` and `useAuth` hook. I understood how to use `useEffect` in the
    provider for initial asynchronous state initialization. I learned how to refactor
    components to consume a global context. I successfully implemented robust
    client-side route protection logic that relies on global authentication state.
    I integrated API service calls (login, logout, fetch user) with global state
    updates. I reinforced that complex patterns often require learning from external
    resources and that understanding can deepen through review and use. I learned how
    to create and use shared UI components that depend on global application state.

---

## 2025-05-05 - Product Catalog Backend

-   **General:** Today, I started working on the Product Catalog milestone. I focused
    on building the core backend pieces for managing products and categories.

-   **Backend:**
    * I created the `Product` and `Category` models.
    * I created DRF `serializers` for both models to handle data conversion to/from JSON.
        I configured the `ProductSerializer` to nest the `CategorySerializer` for
        read operations, showing full category details instead of just the ID.
    * I created DRF `ViewSets` for `Product` and `Category`. I implemented list and
        retrieve views. I used `ModelViewSet` which provides these automatically.
    * I learned that I can make multiple commits locally before pushing them all
        at once to the remote repository.

-   **Learning:** I gained experience defining Django models with relationships.
    I learned how to create DRF `ModelSerializers` and use nested serializers for
    representing related data. I practiced using `ModelViewSet` for standard API
    endpoints like list and retrieve.

---

## 2025-05-06 - Product Detail Frontend

-   **General:** Today, I worked on creating the frontend page for displaying individual
    product details. It felt relatively straightforward.

-   **Frontend:**
    * I created the `ProductDetailPage` component.
    * The main challenge was handling the passing of the product `id` as a
        parameter for routing. I initially tried using props, which didn't work
        for this. Then, I used `useParams` (from a React Router context, which I
        likely needed to figure out how to use with Next.js's App Router), which
        worked, but I want to revisit this to ensure it's the correct Next.js App
        Router method later.
    * The coding logic for fetching and displaying the data was fairly simple
        once the parameter passing was figured out.

-   **Learning:** I gained initial experience with client-side routing and how to
    extract parameters from the URL to fetch data for a specific item. I realized
    the importance of understanding the specific routing method used by the
    framework (Next.js App Router in this case).

---

## 2025-05-07 - Frontend Restructure & Shopping Cart Backend

-   **General:** Today, I started tackling features related to the Shopping Cart
    (Milestone 3 according to the plan). This involved some necessary frontend
    restructuring and significant backend work on the core cart logic.

-   **Frontend:**
    * I implemented a button on the product list view that navigates to the
        product detail page. Again, I faced a challenge with passing the product ID
        as a parameter specifically through the `onClick` event handler, requiring
        me to look up how to do this correctly in React/JSX. The rest of the navigation
        logic felt intuitive.
    * **Restructured the project:** I decided to move components and project files
        out of the `src/app/` directory and place them directly under `src/`. The
        new structure under `src/` now includes `app/` (only for page routes),
        `context/`, `services/`, `ui/` (for components, I was planning to rename to `pages/`
        but unsure if this is the correct term for route components), and `type.ts`
        (for TypeScript definitions). Other library or feature components will be
        added to `src/` as needed.

-   **Backend:**
    * **Learning:** I gained practical experience in creating and configuring a new
        Django app (`cart`) specifically for the shopping cart feature, separating
        it from the `products` app. I learned how to move models between apps (if
        any were initially placed elsewhere) and update imports and migrations
        accordingly.
    * I implemented serializers for models with Foreign Key relationships and nested
        representations (`CartSerializer` including `CartItemSerializer`,
        `CartItemSerializer` including `ProductSerializer`).
    * I used `PrimaryKeyRelatedField` with `write_only=True` to handle foreign key
        assignment (like adding a product to a cart item) based on a provided ID
        in the incoming data.
    * I developed custom API views (`APIView`) and overrode `ModelViewSet` methods
        for specific logic related to the cart (e.g., adding/updating item quantity,
        filtering the queryset to show only the current user's cart, validating
        quantity on update).
    * I used `transaction.atomic` for database integrity during complex add/update
        operations involving multiple database changes.
    * I configured URLs for complex API structures using `DefaultRouter` and explicit
        `path` mappings to handle different cart actions.
    * I practiced testing authenticated API endpoints related to the cart using
        Insomnia/curl.
    * I debugged Django/DRF errors related to model managers, serializer Meta classes,
        and other issues.

---

## 2025-05-08 - Frontend Cart - Add to Cart Button & Token Retrieval

**General**: I started implementing the "Add to Cart" button on the Product Detail page
and connecting it to the backend API. I hit a major roadblock with securely getting
the authentication token on the frontend.

### Frontend:
- I added an "Add to Cart" button to the `ProductDetailPage`.
- I started implementing the `handleAddToCart` click handler.
- I created the `addItemToCart` service function in `product-service.ts` to make
  the `POST` request to `/api/cart/items/`.

**Problem**: I realized the `addItemToCart` function needed the JWT access token string
for the `Authorization: Bearer` header, but the token is in an HttpOnly cookie and
not directly accessible by client-side JavaScript.

**Learning**: I understood the security implications of HttpOnly cookies and why
the token string isn't directly available on the client side. I realized a secure
method is needed to retrieve the token for API headers.

### Backend:
**Solution**: I created a new backend API endpoint (`GET /auth/get-token/`) in the
`accounts` app. This endpoint:
- Is called by the authenticated frontend (the cookie is sent automatically).
- Reads the token from the HttpOnly cookie.
- Returns the token string in the response body.

I added the corresponding URL pattern in `accounts/urls.py`.

**Learning**: I learned the standard and secure pattern for providing the JWT token
string to the frontend when using HttpOnly cookies by creating a dedicated backend
endpoint.

---

## 2025-05-09 - Debugging Token Retrieval & Custom Authentication

**General**: I spent the day debugging issues with the new backend token retrieval
endpoint, which was preventing the "Add to Cart" functionality from working.

### Frontend:
- I updated the `getAuthToken` function in `auth.ts` to call the new backend
  `GET /auth/get-token/` endpoint.
- I updated `addItemToCart` in `product-service.ts` to use the `getAuthToken` function.
- I updated `ProductDetailPage` to call the `addItemToCart` service.

**Problems**:
1. Testing the `GET /auth/get-token/` endpoint resulted in `401 Unauthorized` errors.
2. I got `"detail": "Method \"GET\" not allowed."` for the `GET` request.

### Backend:
**Solution**: I created a custom `JWTCookieAuthentication` class that:
- Inherits from `JWTAuthentication`.
- Explicitly checks `request.COOKIES` for the token first.
- Updated `settings.py` to include `AUTH_COOKIE` in `SIMPLE_JWT`.

**Learning**: I gained a deep understanding of how JWT authentication works with
HttpOnly cookies in Django/DRF, especially the need for custom authentication
classes to read the cookie.

---

## 2025-05-10 - Frontend Auth - Login Fix & Cart Page (Fetch/Display)

**General**: I fixed a bug in the login form and successfully implemented the
frontend Cart Page.

### Frontend:
**Problem**: The login form threw `TypeError: user is undefined` on `loginSuccess(user)`.

**Solution**: I updated `handleSubmit` to call `WorkspaceAuthenticatedUser()` after
a successful login to ensure the `user` object was properly fetched and available
before updating the global state.

**Cart Page Implementation**:
- I created the `CartPage` component (`app/cart/page.tsx`).
- I created `cart-service.ts` with the `WorkspaceCart` function.
- I implemented a `useEffect` in `CartPage` to call `WorkspaceCart()` when the component
  mounts.
- I added loading states, error handling, and logic to display the cart contents.

**Learning**: I learned to debug frontend errors by tracing undefined values and
gained experience in structuring new page components for data fetching and display.

---

## 2025-05-11 - Frontend Cart - Update/Remove & Debugging

**General**: I implemented functionality to update item quantities and remove
items from the cart.

### Frontend:
- I added `updateCartItemQuantity` and `removeCartItem` functions to `cart-service.ts`.
- I added quantity controls (`+/-` buttons) and a "Remove" button to `CartPage`.
- I implemented handlers for updating and removing items.
- I added local state updates after successful API calls (using the `setCart(prevCart => { ... })`
  pattern for efficient UI updates without a full page reload).

**Problems**:
1. The number input for quantity behaved erratically, so I switched to `+/-` buttons
   for a better user experience.
2. The "Remove" button caused a `500 Internal Server Error` on the backend.

### Backend:
**Solution**: The `500` error was due to a missing trailing slash in the `DELETE`
request URL to the `CartItemViewSet`. I fixed this by ensuring the URL in the
`removeCartItem` function included the trailing slash.

**Learning**: I gained experience with:
- Updating/deleting items in a list in the UI.
- Handling UI state during asynchronous operations to provide immediate feedback
  to the user (e.g., disabling buttons while an update is in progress).
- Debugging frontend-triggered backend errors by inspecting network requests and
  backend logs/tracebacks.

---

## 2025-05-12 - Backend: Order Creation & History Models/API

-   **General:** I started implementing the core backend logic for turning a user's
    cart into a formal order and providing a way to view past orders. This involved
    creating new Django models and setting up a new API endpoint.

-   **Backend:**
    * **New App:** I created a new Django app called `orders` using
      `python manage.py startapp orders` to keep order-related logic separate
      and organized.
    * **Models:** I defined the `Order` model (linked to `User`, with fields for
      `total_amount`, `status`, `created_at`, `updated_at`) and the `OrderItem`
      model (linked to `Order` and `Product`, specifically storing `product_name`,
      `product_price`, and `quantity` at the time of order for historical accuracy).
    * I ran `python manage.py makemigrations` and `python manage.py migrate` to create
      the new database tables.
    * **Serializers:** I created `OrderItemSerializer` and `OrderSerializer` in
      `orders/serializers.py`. I learned about **nested serializers** here,
      specifically how to include `OrderItemSerializer(many=True, read_only=True)`
      inside `OrderSerializer` to represent all items belonging to an order in the
      API response. I also nested `ProductSerializer` inside `OrderItemSerializer`
      for full product details.
    * **Order Creation API:** I implemented a new `OrderListCreateView` in
      `orders/views.py` using `generics.ListCreateAPIView`.
        * This view handles `POST` requests to create an order from the
          authenticated user's cart.
        * It fetches the user's current cart and its items.
        * It uses `django.db.transaction.atomic()` to ensure **database integrity**:
          if any step of order creation (creating `Order`, creating `OrderItem`s,
          clearing `CartItem`s) fails, all changes are rolled back. This was a
          critical learning point for reliable transactions.
        * It iterates through `CartItem`s, creates `OrderItem`s (copying product
          details), calculates the total, saves the `Order`, and then clears the
          `CartItem`s.
    * **Order Listing API:** The `OrderListCreateView` also inherently handles
      `GET` requests to `/api/orders/`, returning a list of all orders for the
      authenticated user via its `get_queryset` method.
    * **URLs:** I configured `urls.py` in the new `orders` app and included it in
      the main project `urls.py` under `/api/orders/`.

-   **Learning:** I gained significant experience with:
    * Structuring Django apps for modularity.
    * Defining models with complex relationships and considering historical data
      (e.g., `product_price` on `OrderItem`).
    * Implementing DRF serializers with nesting for rich API responses.
    * Using `django.db.transaction.atomic` for robust database operations.
    * Leveraging `generics.ListCreateAPIView` to handle both listing and creation
      with less boilerplate.

---

## 2025-05-13 - Backend: Debugging Order Creation & Frontend: Checkout Button

-   **General:** I debugged a critical error in the backend order creation process
    and then started connecting the frontend Cart page to the new backend order API.

-   **Backend:**
    * *Problem:* I encountered an `IntegrityError: null value in column "total_amount"
      of relation "orders_order" violates not-null constraint` when trying to create
      an order.
    * *Solution:* I realized that `Order.objects.create()` immediately saves the
      instance, but `total_amount` was calculated *after* this initial save. The fix
      was to instantiate the `Order` object (`order = Order(...)`) without immediately
      saving it, calculate `total_amount`, assign it, and *then* call `order.save()`
      within the `transaction.atomic()` block. This ensured `total_amount` was present
      on the first save.
    * I tested the `POST /api/orders/` endpoint successfully using Insomnia/curl
      after the fix.

-   **Frontend:**
    * **Checkout Button:** I added a "Proceed to Checkout" button to the `CartPage`
      component (`app/cart/page.tsx`).
    * **Order Service:** I created a new service file `ecommerce_frontend/src/services/order-service.ts`.
    * I implemented the `createOrder` asynchronous function in `order-service.ts`.
      This function handles the `POST` request to `/api/orders/`, including getting
      the authentication token and robust error handling.
    * I connected the "Proceed to Checkout" button's `onClick` handler (`handleCheckout`)
      to call the `createOrder` service function.
    * I implemented state management (`isCheckingOut`, `checkoutMessage`) to show
      loading status and success/failure messages on the Cart page.
    * Upon successful order creation, the `handleCheckout` function now clears the
      local cart state (`setCart(null)`) and displays a success message like
      "Order #X created successfully!" on the Cart page, keeping the user on the
      same page.

-   **Learning:** I deepened my understanding of database integrity errors and how
    to correctly sequence object creation and saving in Django. I gained practical
    experience integrating frontend button clicks with backend API calls, managing
    UI loading states, and providing user feedback for complex operations like checkout.

---

## 2025-05-14 - Frontend: Order History Page

-   **General:** I created the frontend page to display a user's past orders,
    connecting it to the backend's order listing API.

-   **Frontend:**
    * **New Page:** I created the `OrderHistoryPage` component at
      `ecommerce_frontend/src/app/orders/page.tsx`.
    * **Fetch Orders Service:** I added the `WorkspaceOrders` asynchronous function to
      `ecommerce_frontend/src/services/order-service.ts`. This function makes a `GET`
      request to `/api/orders/`, retrieves the list of orders, and handles authentication.
    * **Data Display:** I implemented a `useEffect` in `OrderHistoryPage` to call
      `WorkspaceOrders()` when the component loads.
    * I displayed the fetched orders in a user-friendly format, including order
      details (ID, date, status, total) and a nested list of `OrderItem`s, showing
      product name, price, and quantity for each.
    * I included loading states and error handling for the order history display.
    * I ensured proper authentication checks: the page prompts the user to log in
      if they are not authenticated, preventing unauthorized access to order history.

-   **Learning:** I learned how to create new pages in Next.js App Router that fetch
    and display lists of data from a backend API. I practiced using `useEffect` for
    data loading and conditional rendering based on loading, error, and
    authentication states. I solidified my understanding of how to display nested
    data structures (orders with their items).

---

## 2025-05-15 - Backend: Admin Enhancements (Products, Cart, Orders)

-   **General:** Today, I focused on making the Django Admin interface much more
    user-friendly and and powerful for managing the e-commerce data.

-   **Backend:**
    * **Products Admin (`products/admin.py`):**
        * I registered `Product` and `Category` models with custom `ModelAdmin` classes.
        * I used `list_display` to show relevant columns (name, category, price,
          stock, timestamps).
        * I added `list_filter` for `category` and timestamps.
        * I implemented `search_fields` for `name`, `description`, and
          `category__name` to enable searching products directly in the Admin.
    * **Cart Admin (`cart/admin.py`):**
        * I registered `Cart` and `CartItem` models.
        * I implemented `CartItemInline` using `admin.TabularInline` to display
          `CartItem`s directly on the `Cart` detail page, making it easy to see
          what's in a user's cart.
        * I customized `CartAdmin` with `list_display`, `list_filter`, and
          `search_fields` (by `user__username`).
    * **Orders Admin (`orders/admin.py`):**
        * I registered `Order` and `OrderItem` models.
        * I implemented `OrderItemInline` to display `OrderItem`s directly on the
          `Order` detail page, showing the historical record of items in an order.
        * I customized `OrderAdmin` with `list_display`, `list_filter` (by `status`,
          timestamps), and `search_fields` (by `id`, `user__username`).
        * I made `user`, `total_amount`, and timestamps `readonly_fields` in
          `OrderAdmin` as they are set by the system.
    * **Custom Admin Action:** I added a custom action to `OrderAdmin` called
      `mark_as_processing`.
        * This function allows me to select multiple orders from the list view and
          bulk update their `status` to 'Processing'.
        * I used `queryset.update()` for efficient bulk database operations and
          `self.message_user()` to provide feedback in the Admin interface.

-   **Learning:** I gained extensive practical experience with Django Admin
    customization. I learned to use `admin.ModelAdmin` attributes like
    `list_display`, `list_filter`, `search_fields`, `readonly_fields`. I
    understood the power of `admin.TabularInline` for managing related objects
    on a single page. I successfully implemented a custom Admin action, which is
    a very useful feature for bulk operations.

---

## 2025-05-16 - Backend: Product Search & Filter Implementation

-   **General:** I started implementing search and filtering capabilities for
    products on the backend API.

-   **Backend:**
    * **Install `django-filter`:** I installed the `django-filter` library
      (`pip install django-filter`) and added `'django_filters'` to
      `INSTALLED_APPS` in `settings.py`.
    * **`ProductViewSet` Enhancement:** I modified the `ProductViewSet` in
      `products/views.py`.
        * I added `filter_backends = [DjangoFilterBackend, filters.SearchFilter]`.
        * I configured `DjangoFilterBackend` using `filterset_fields = ['category']`
          to allow filtering products by category ID (e.g., `/api/products/?category=1`).
        * I configured `SearchFilter` using `search_fields = ['name', 'description']`
          to enable text-based search on product name and description (e.g.,
          `/api/products/?search=laptop`).
    * I tested the `GET /api/products/` endpoint with `?search=` and `?category=`
      parameters using Insomnia/curl, confirming that the backend was correctly
      filtering and searching the products.

-   **Learning:** I learned how to easily add powerful search and filtering to
    DRF API endpoints using `django-filter` and `rest_framework.filters.SearchFilter`.
    I understood the role of `filter_backends`, `filterset_fields`, and
    `search_fields` in configuring these features.

---

## 2025-05-17 - Frontend: Product Search & Filter UI & Logic

-   **General:** I built the frontend user interface for product search and
    filtering and connected it to the enhanced backend API.

-   **Frontend:**
    * **UI Elements:** I added a text `input` field for search and a `select`
      dropdown for category filtering to the `ProductsPage` component
      (`app/products/page.tsx`).
    * **URL Parameter Sync:** I used `useRouter` and `useSearchParams` from
      Next.js to read initial search/category parameters from the URL and to
      update the URL when filters are applied.
    * **Data Fetching with Parameters:** I modified the `WorkspaceProducts` service
      function in `product-service.ts` to accept `searchTerm` and `categoryId`
      parameters and include them in the API request URL using `URLSearchParams`.
    * **Category Fetching:** I added a new `WorkspaceCategories` service function to
      `product-service.ts` to populate the category dropdown dynamically from the
      backend.
    * **`useEffect` for Re-fetching:** I configured the main `useEffect` in
      `ProductsPage` to re-fetch products whenever `searchTerm` or `selectedCategory`
      changes, ensuring the displayed list updates.
    * **"Apply Filters" Button:** I implemented a button that, when clicked,
      updates the browser's URL with the current `searchTerm` and `selectedCategory`,
      which in turn triggers the `useEffect` to re-fetch products.

-   **Learning:** I gained practical experience with:
    * Building interactive search and filter UI components in React/Next.js.
    * Using `useRouter` and `useSearchParams` for client-side URL manipulation
      and state synchronization.
    * Passing query parameters to backend API calls from the frontend.
    * Dynamically populating dropdowns from API data.

---

## 2025-05-18 - Frontend: Debouncing Search Input for UX

-   **General:** I addressed a significant user experience issue with the product
    search bar, where typing caused constant re-renders and loss of input focus.

-   **Frontend:**
    * **Problem:** The search input field was losing focus and "blinking" with
      every keystroke because `searchTerm` was updated immediately, triggering a
      re-render and API call.
    * **Solution: Debouncing:** I implemented **debouncing** for the search input.
        * I introduced a `localSearchTerm` state variable to hold the input field's
          value as the user types.
        * The `<input>`'s `value` is now bound to `localSearchTerm`, and `onChange`
          updates `setLocalSearchTerm`.
        * A new `useEffect` was added that uses `setTimeout` to update the *actual*
          `searchTerm` (which triggers the API call) only after `localSearchTerm`
          has stopped changing for 500 milliseconds.
        * A `clearTimeout` cleanup function was added to prevent unnecessary API
          calls if the user types quickly.
    * The "Apply Filters" button still uses the debounced `searchTerm` for the
      final filter application.

-   **Learning:** I learned about and successfully implemented **debouncing** as a
    crucial technique for improving user experience in input fields that trigger
    expensive operations (like API calls). I understood the `setTimeout` and
    `clearTimeout` pattern within `useEffect` for effective debouncing. This was a
    direct solution to a real-world UI problem, which felt very rewarding.
