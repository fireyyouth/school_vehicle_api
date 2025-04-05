rm main/migrations/0* && rm db.sqlite3 &&  \
    ./manage.py makemigrations && \
    ./manage.py migrate && \
    ./manage.py shell < populate_data.py

