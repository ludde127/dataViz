# Append git hash to env file
grep -q '^GIT_HASH\s*=.*' .yapenv.production \
	&& sed -i "s/^GIT_HASH\s*=.*/GIT_HASH=$(git rev-parse --short HEAD)/" .yapenv.production \
	|| echo "GIT_HASH=$(git rev-parse --short HEAD)" >> .yapenv.production

venv/bin/pip install -r ./requirements.txt
venv/bin/python ./manage.py makemigrations && venv/bin/python ./manage.py migrate
venv/bin/python ./manage.py update_index
venv/bin/python ./manage.py collectstatic --no-input
systemctl restart yapity.service
