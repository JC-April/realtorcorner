set -o errexit #exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell -c "import create_superuser; create_superuser.create_superuser()"