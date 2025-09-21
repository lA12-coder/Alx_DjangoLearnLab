# LibraryProject/bookshelf/middleware.py
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Adds common security headers, including a Content-Security-Policy (CSP).
    This is a simple approach. For complex CSP needs consider 'django-csp' package.
    """

    def _csp_value(self):
        # Build CSP from settings (tweak as needed)
        default_src = " ".join(settings.CSP_DEFAULT_SRC) if hasattr(settings, 'CSP_DEFAULT_SRC') else "'self'"
        script_src = " ".join(getattr(settings, 'CSP_SCRIPT_SRC', ("'self'",)))
        style_src = " ".join(getattr(settings, 'CSP_STYLE_SRC', ("'self'",)))
        img_src = " ".join(getattr(settings, 'CSP_IMG_SRC', ("'self'", "data:")))
        font_src = " ".join(getattr(settings, 'CSP_FONT_SRC', ("'self'",)))
        connect_src = " ".join(getattr(settings, 'CSP_CONNECT_SRC', ("'self'",)))

        parts = [
            f"default-src {default_src};",
            f"script-src {script_src};",
            f"style-src {style_src};",
            f"img-src {img_src};",
            f"font-src {font_src};",
            f"connect-src {connect_src};",
        ]
        return " ".join(parts)

    def process_response(self, request, response):
        # Add CSP header if not present
        if not response.has_header('Content-Security-Policy'):
            response['Content-Security-Policy'] = self._csp_value()

        # Add other security headers (redundant with proper settings but explicit)
        if not response.has_header('X-Content-Type-Options'):
            response['X-Content-Type-Options'] = 'nosniff'
        if not response.has_header('X-Frame-Options'):
            response['X-Frame-Options'] = getattr(settings, 'X_FRAME_OPTIONS', 'DENY')
        # X-XSS-Protection is deprecated in modern browsers but we can set for older ones
        if not response.has_header('X-XSS-Protection'):
            response['X-XSS-Protection'] = '1; mode=block'
        return response
