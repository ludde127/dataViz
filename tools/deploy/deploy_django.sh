venv/bin/pip install -r ./requirements.txt
venv/bin/python ./manage.py makemigrations && venv/bin/python ./manage.py migrate
venv/bin/python ./manage.py collectstatic --no-input
systemctl restart yapity.service
