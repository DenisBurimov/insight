sleep 2
echo Run db upgrade
flask db upgrade
echo Run app server
gunicorn -w 4 -b 0.0.0.0:8080 'wsgi:app'
