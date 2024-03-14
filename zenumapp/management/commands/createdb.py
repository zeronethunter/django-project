import random
import string

from django.core.management.base import BaseCommand, CommandError
from zenumapp.models import Question, Answer, Profile, User, Rating
from py_random_words import random_words
from django.utils.timezone import now
from django.utils import lorem_ipsum


def random_string(start, end):
    number = random.randint(start, end)
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=number))


def generate_random(u_count, q_count, a_max_count, r_per_question):
    rnd_words = random_words.RandomWords()
    for i in range(u_count):
        user = User.objects.create_user(username=random_string(5, 25),
                                        email='{0}@{1}.ru'.format(random_string(10, 25), random_string(2, 5)),
                                        password="test")
        Profile.objects.create(user=user)
    for j in range(q_count):
        question_user = User.objects.all()[random.randint(0, u_count - 1)]

        q = Question.objects.create(question_title=random_string(10, 25),
                                    question_text=lorem_ipsum.words(random.randint(20, 100)),
                                    views=random.randint(1, q_count),
                                    pub_date=now(), user=question_user, is_hot=random.randint(0, 1))
        q.tags.add(rnd_words.get_word(), rnd_words.get_word(), rnd_words.get_word())

        random_answers = random.randint(2, a_max_count)
        random_right_answer = random.randint(0, random_answers - 1)
        for g in range(random_answers):
            if j == random_right_answer:
                a = Answer.objects.create(
                    answer_text=lorem_ipsum.words(random.randint(50, 100)), question=q,
                    pub_date=now(), is_right=True,
                    user=User.objects.exclude(username=question_user.username)[
                        random.randint(0, u_count - 1)])
            else:
                a = Answer.objects.create(
                    answer_text=lorem_ipsum.words(random.randint(50, 100)), question=q,
                    pub_date=now(), is_right=False,
                    user=User.objects.exclude(username=question_user.username)[
                        random.randint(0, u_count - 1)])

        for ratings in range(random.randint(1, r_per_question)):
            score = random.randint(0, 1)
            if score:
                Rating.objects.create(up_vote=True, down_vote=False,
                                      question=Question.objects.all()[
                                          random.randint(0, Question.objects.count() - 1)],
                                      answer=Answer.objects.all()[
                                          random.randint(0, Answer.objects.count() - 1)])
            else:
                Rating.objects.create(up_vote=False, down_vote=True,
                                      question=Question.objects.all()[
                                          random.randint(0, Question.objects.count() - 1)],
                                      answer=Answer.objects.all()[
                                          random.randint(0, Answer.objects.count() - 1)])


class Command(BaseCommand):
    help = 'Creates db witch need in task'

    def add_arguments(self, parser):
        parser.add_argument('count_users', nargs='+', type=int)
        parser.add_argument('count_questions', nargs='+', type=int)
        parser.add_argument('max_answers_per_question', nargs='+', type=int)
        parser.add_argument('ratings_per_question', nargs='+', type=int)

    def handle(self, *args, **options):
        generate_random(options['count_users'][0], options['count_questions'][0],
                        options['max_answers_per_question'][0],
                        options['ratings_per_question'][0])
