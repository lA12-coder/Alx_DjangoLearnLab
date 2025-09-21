# Security Review — HTTPS & Secure Redirects

Date: 2025-09-21

## Summary

Implemented configuration changes in `LibraryProject/LibraryProject/settings.py` to enforce HTTPS traffic, enable HSTS, secure cookies, and strong security-related headers.

## What was changed

- Read `SECRET_KEY` and `DEBUG` from environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`).
- `ALLOWED_HOSTS` is now set from `DJANGO_ALLOWED_HOSTS` environment variable.
- Enforced secure cookies: `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`.
- Set `SECURE_SSL_REDIRECT = True` to redirect HTTP -> HTTPS.
- Enabled HSTS with `SECURE_HSTS_SECONDS` (default 31536000), `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`, and `SECURE_HSTS_PRELOAD = True`.
- Added `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` for reverse proxies.
- Enabled headers: `X_FRAME_OPTIONS = 'DENY'`, `SECURE_CONTENT_TYPE_NOSNIFF = True`, `SECURE_BROWSER_XSS_FILTER = True`.

## Notes and caveats

- `SECURE_HSTS_SECONDS = 31536000` (one year) is aggressive for a first deployment. Consider starting with a small value like 60 and increasing after verifying HTTPS is working correctly.
- `SECURE_SSL_REDIRECT = True` will make the app redirect all HTTP traffic to HTTPS — ensure HTTPS is correctly configured on your server or load balancer before enabling.
- `CSRF_COOKIE_HTTPONLY = True` prevents JavaScript from reading the CSRF cookie. If your frontend relies on reading the cookie, update your frontend to obtain the token in another safe way (e.g., render it into templates or provide an endpoint).
- `SECRET_KEY` must be kept secret and should not appear in source control.

## Next steps

- Update deployment automation to set the required environment variables (`DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_DEBUG`, and optionally `SECURE_HSTS_SECONDS`).
- Install an SSL certificate via Let's Encrypt (see `DEPLOYMENT.md`) or use a managed certificate.
- Re-run `python manage.py check --deploy` after installing any missing Python dependencies (e.g., Pillow for `ImageField`).
