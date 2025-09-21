Security Measures Summary (LibraryProject)
-----------------------------------------

1. Settings (production):
   - DEBUG = False
   - SESSION_COOKIE_SECURE = True
   - CSRF_COOKIE_SECURE = True
   - SESSION_COOKIE_HTTPONLY = True
   - SECURE_CONTENT_TYPE_NOSNIFF = True
   - SECURE_BROWSER_XSS_FILTER = True
   - X_FRAME_OPTIONS = 'DENY'
   - SECURE_HSTS_SECONDS set in production

2. CSRF Protection:
   - All POST forms include {% csrf_token %}.

3. Input validation & SQL safety:
   - Use Django ModelForms (BookForm) for validation.
   - Use Django ORM (filter/Q) instead of string SQL.
   - If raw SQL is used, pass parameters via placeholders (never format strings).

4. Content Security Policy:
   - SecurityHeadersMiddleware adds CSP header.
   - For complex per-view CSP consider 'django-csp' package.

5. Middleware:
   - bookshelf.middleware.SecurityHeadersMiddleware is installed to add CSP and other headers.

6. Testing:
   - Manual tests for CSRF, XSS, SQL injection attempts and cookie flags recommended.
