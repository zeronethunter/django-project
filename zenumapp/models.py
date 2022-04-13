import random
import string

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import lorem_ipsum
from taggit.managers import TaggableManager
from py_random_words import random_words


def random_string(start, end):
    number = random.randint(start, end)
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=number))


class QuestionManager(models.Manager):
    def select_by_tag(self, tag_name):
        return Question.objects.filter(tags__name=tag_name)


def generate_random(u_count, q_count, a_max_count):
    rnd_words = random_words.RandomWords()
    for i in range(u_count):
        user = User.objects.create_user(username=random_string(5, 25),
                                        email='{0}@{1}.ru'.format(random_string(10, 25), random_string(2, 5)),
                                        password=random_string(15, 25))
        Profile.objects.create(user=user)
    for j in range(q_count):
        question_user = User.objects.all()[random.randint(0, u_count - 1)]

        q = Question.objects.create(question_title=random_string(10, 25),
                                    question_text=lorem_ipsum.words(random.randint(20, 100)),
                                    views=random.randint(1, q_count),
                                    pub_date=now(), user=question_user)
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

        for ratings in range(random.randint(1, 20)):
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


class ProfileManager(models.Manager):
    def get_user(self, user_name):
        return Profile.objects.get(user=user_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.email


class Question(models.Model):
    question_title = models.CharField(max_length=64)
    question_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    views = models.PositiveIntegerField()
    tags = TaggableManager()
    pub_date = models.DateTimeField(blank=True)
    last_update = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def is_answered(self):
        if self.answers.filter(is_right=True):
            return True
        else:
            return False

    def get_answers(self):
        return self.answers.all()

    def count_answers(self):
        return self.answers.count()

    def __str__(self):
        return self.question_title


class Answer(models.Model):
    answer_text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    is_right = models.BooleanField()
    pub_date = models.DateTimeField(blank=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text


class Rating(models.Model):
    # 1 if voted, 0 if not
    up_vote = models.BooleanField()
    down_vote = models.BooleanField()

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rating', null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='rating')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return str(self.vote)
