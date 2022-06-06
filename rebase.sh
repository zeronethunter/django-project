#Set path to project
LOCAL_PATH=/home/zenehu/Dev/PycharmProjects/forum_task/
MIGRATIONS_PATH=${LOCAL_PATH}zenumapp/migrations/

# Configure DB creation here
USER_COUNT=10
QUESTION_COUNT=100
MAX_COUNT_ANSWERS_IN_QUESTION=20
COUNT_RATING_PER_QUESTION=20

sudo rm ${MIGRATIONS_PATH}0001_initial.py
sudo rm ${LOCAL_PATH}db.sqlite3

python3 ${LOCAL_PATH}manage.py makemigrations
python3 ${LOCAL_PATH}manage.py migrate
python3 ${LOCAL_PATH}manage.py sqlmigrate zenumapp 0001
python3 ${LOCAL_PATH}manage.py createsuperuser
echo "Wait until db will be created..."
python3 ${LOCAL_PATH}manage.py createdb ${USER_COUNT} ${QUESTION_COUNT} ${MAX_COUNT_ANSWERS_IN_QUESTION} ${COUNT_RATING_PER_QUESTION}
echo "Success"

python3 ${LOCAL_PATH}manage.py runserver
