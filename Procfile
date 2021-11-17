release: python3 manage.py makemigrations
release: python3 manage.py migrate
release: python3 manage.py runcrons
web: gunicorn evolves.wsgi --preload --log-file -