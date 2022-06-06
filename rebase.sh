LOCAL_PATH=/home/zenehu/Dev/PycharmProjects/forum_task/
MIGRATIONS_PATH=/home/zenehu/Dev/PycharmProjects/forum_task/zenumapp/migrations/

sudo rm ${MIGRATIONS_PATH}0001_initial.py
sudo rm ${LOCAL_PATH}db.sqlite3

python3 ${LOCAL_PATH}manage.py makemigrations
python3 ${LOCAL_PATH}manage.py migrate
python3 ${LOCAL_PATH}manage.py sqlmigrate zenumapp 0001
python3 ${LOCAL_PATH}manage.py createsuperuser
