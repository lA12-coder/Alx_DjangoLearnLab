# Deployment: Enabling HTTPS (Nginx + Gunicorn example)

This document shows an example Nginx configuration and steps to enable HTTPS using Let's Encrypt (Certbot). Adjust paths and service names for your environment.

## 1. Install Certbot

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

## 2. Example Nginx site configuration

Replace `example.com` with your domain and adjust file paths.

```
server {
    listen 80;
    server_name example.com www.example.com;

    location /static/ {
        alias /path/to/your/project/static/;
    }

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Reload Nginx and obtain certificates using Certbot:

```bash
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d example.com -d www.example.com
```

Certbot will update your Nginx config to listen on 443 and use the certificates.

## 3. Gunicorn systemd service example

Create `/etc/systemd/system/gunicorn.service`:

```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock LibraryProject.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start Gunicorn:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn
```

## 4. Notes

- Ensure Django's `ALLOWED_HOSTS` includes your domain (or set via `DJANGO_ALLOWED_HOSTS` env var).
- Ensure `DJANGO_SECRET_KEY` is set in the environment for production.
- `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, and other security settings are set in `settings.py`. Adjust `SECURE_HSTS_SECONDS` to a low value (e.g., 60) for initial testing.
- If behind a proxy, ensure `SECURE_PROXY_SSL_HEADER` is configured and Nginx forwards `X-Forwarded-Proto`.
