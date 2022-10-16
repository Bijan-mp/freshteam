echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT ; do
  sleep 0.1
done

echo "PostgreSQL started"
echo "Waiting for server to RUN"
cd /app/src
python3 manage.py migrate --noinput
python3 manage.py  runserver 0.0.0.0:8000