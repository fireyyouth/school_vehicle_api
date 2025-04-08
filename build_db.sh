rm -f */migrations/0* && rm -f db.sqlite3 &&  \
    ./manage.py makemigrations && \
    ./manage.py migrate && \
    ./manage.py shell < populate_data.py

