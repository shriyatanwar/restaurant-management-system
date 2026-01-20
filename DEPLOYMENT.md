# Deployment Guide - Restaurant Management System

This guide covers deploying the Restaurant Management System to production.

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Database migrations created and tested
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] Secret key changed from default
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured
- [ ] Database backups configured
- [ ] SSL certificate obtained (for HTTPS)

## Production Environment Setup

### 1. Server Requirements

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 2GB
- Storage: 20GB
- OS: Ubuntu 20.04 LTS or newer

**Recommended:**
- CPU: 4 cores
- RAM: 4GB
- Storage: 50GB

### 2. Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and PostgreSQL
sudo apt install python3.10 python3.10-venv python3-pip postgresql postgresql-contrib nginx -y

# Install additional dependencies
sudo apt install libpq-dev python3-dev build-essential -y
```

### 3. Setup PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE restaurant_db;
CREATE USER restaurant_user WITH PASSWORD 'your_secure_password';
ALTER ROLE restaurant_user SET client_encoding TO 'utf8';
ALTER ROLE restaurant_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE restaurant_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO restaurant_user;
\q
```

### 4. Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/restaurant
sudo chown $USER:$USER /var/www/restaurant
cd /var/www/restaurant

# Clone or copy your application
# git clone <your-repo> .
# Or copy files manually

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 5. Configure Environment Variables

Create production `.env` file:

```bash
nano /var/www/restaurant/.env
```

```env
# Production settings
SECRET_KEY=<generate-strong-random-key-here>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your.server.ip

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=restaurant_db
DB_USER=restaurant_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

**Generate a secure SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Run Migrations and Collect Static Files

```bash
cd /var/www/restaurant
source venv/bin/activate

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --no-input

# Test the application
python manage.py check --deploy
```

## Application Server Setup (Gunicorn)

### 1. Create Gunicorn Configuration

```bash
sudo nano /etc/systemd/system/restaurant.service
```

```ini
[Unit]
Description=Restaurant Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/restaurant
Environment="PATH=/var/www/restaurant/venv/bin"
ExecStart=/var/www/restaurant/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/restaurant/restaurant.sock \
          restaurant.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 2. Set Permissions

```bash
sudo chown -R www-data:www-data /var/www/restaurant
sudo chmod -R 755 /var/www/restaurant
```

### 3. Start Gunicorn Service

```bash
sudo systemctl start restaurant
sudo systemctl enable restaurant
sudo systemctl status restaurant
```

## Web Server Setup (Nginx)

### 1. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/restaurant
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/restaurant/staticfiles/;
    }

    location /media/ {
        alias /var/www/restaurant/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/restaurant/restaurant.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

### 2. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/restaurant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL Certificate (HTTPS)

### Using Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal:
sudo certbot renew --dry-run
```

## Security Hardening

### 1. Firewall Configuration

```bash
# Enable UFW
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### 2. Update Django Settings

Add to `restaurant/settings.py`:

```python
# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 3. Database Backups

Create backup script:

```bash
sudo nano /usr/local/bin/backup-restaurant-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/restaurant"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

pg_dump -U restaurant_user restaurant_db | gzip > $BACKUP_DIR/restaurant_db_$DATE.sql.gz

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

```bash
sudo chmod +x /usr/local/bin/backup-restaurant-db.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
```

Add line:
```
0 2 * * * /usr/local/bin/backup-restaurant-db.sh
```

## Monitoring and Logging

### 1. Application Logs

```bash
# View Gunicorn logs
sudo journalctl -u restaurant -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Django Logging Configuration

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/restaurant/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

Create log directory:
```bash
sudo mkdir -p /var/log/restaurant
sudo chown www-data:www-data /var/log/restaurant
```

## Maintenance

### Updating Application

```bash
cd /var/www/restaurant
source venv/bin/activate

# Pull latest changes
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Restart services
sudo systemctl restart restaurant
```

### Database Migrations

```bash
cd /var/www/restaurant
source venv/bin/activate

python manage.py makemigrations
python manage.py migrate

sudo systemctl restart restaurant
```

## Performance Optimization

### 1. Enable Database Connection Pooling

Install pgbouncer:
```bash
sudo apt install pgbouncer -y
```

### 2. Add Caching

Install Redis:
```bash
sudo apt install redis-server -y
```

Add to `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

Install Python Redis client:
```bash
pip install django-redis
```

### 3. Optimize Static Files

Use WhiteNoise for serving static files:
```bash
pip install whitenoise
```

Add to `settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## Troubleshooting

### Service Not Starting

```bash
# Check service status
sudo systemctl status restaurant

# Check logs
sudo journalctl -u restaurant -n 50

# Test Gunicorn manually
cd /var/www/restaurant
source venv/bin/activate
gunicorn restaurant.wsgi:application
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -d restaurant_db -U restaurant_user
```

### Static Files Not Loading

```bash
# Recollect static files
cd /var/www/restaurant
source venv/bin/activate
python manage.py collectstatic --clear --no-input

# Check Nginx configuration
sudo nginx -t

# Check file permissions
ls -la /var/www/restaurant/staticfiles/
```

## Scaling Considerations

For high-traffic deployments:

1. **Load Balancing**: Use multiple application servers behind a load balancer
2. **Database Replication**: Setup PostgreSQL primary-replica replication
3. **Caching Layer**: Implement Redis/Memcached for query caching
4. **CDN**: Use CloudFlare or AWS CloudFront for static files
5. **Monitoring**: Implement Prometheus + Grafana or New Relic
6. **Auto-scaling**: Use container orchestration (Docker + Kubernetes)

## Support and Monitoring Services

Consider integrating:
- **Sentry**: Error tracking and monitoring
- **New Relic**: Application performance monitoring
- **Datadog**: Infrastructure monitoring
- **Papertrail**: Log aggregation

## Backup and Disaster Recovery

1. Daily automated database backups
2. Weekly full server snapshots
3. Store backups in off-site location (AWS S3, Google Cloud Storage)
4. Test restoration process quarterly
5. Document recovery procedures

## Conclusion

Your Restaurant Management System is now deployed and secured for production use. Regular maintenance, monitoring, and updates are essential for smooth operation.

For issues or questions, refer to:
- Django deployment documentation
- Gunicorn documentation
- Nginx documentation
- PostgreSQL documentation
