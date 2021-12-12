# Vision

Django backend for Network Performance Monitoring tool.

# Local Deployment

Deploy locally for dev/testing

#### Clone repo

```bash
sudo git clone https://github.com/MrTwister96/vision_project
```

#### Install dependancies

```bash
pip install -r requirements.txt
```

#### Migrations and Start local dev server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

#### Start Celery Beat Worker

```bash
celery -A vision beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

#### Start Celery Worker

```bash
celery -A vision worker -P eventlet -l INFO
```



