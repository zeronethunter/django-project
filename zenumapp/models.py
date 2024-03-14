from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class QuestionManager(models.Manager):
    def select_by_tag(self, tag_name):
        return Question.objects.filter(tags__name=tag_name)


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
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now_add=True)
    is_hot = models.BooleanField()

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

    def get_creator(self):
        return self.user

    def get_rating(self):
        rating = self.rating.all()
        full_rating = 0
        for rate in rating:
            if rate.up_vote:
                full_rating += 1
            elif rate.down_vote:
                full_rating -= 1
        return full_rating

    def get_all_ratings(self):
        return self.rating.all()

    def __str__(self):
        return self.question_title


class Answer(models.Model):
    answer_text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    is_right = models.BooleanField()
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def get_creator(self):
        return self.user

    def get_rating(self):
        rating = self.rating.all()
        full_rating = 0
        for rate in rating:
            if rate.up_vote:
                full_rating += 1
            elif rate.down_vote:
                full_rating -= 1
        return full_rating

    def __str__(self):
        return self.answer_text


class Rating(models.Model):
    # 1 if voted, 0 if not
    up_vote = models.BooleanField()
    down_vote = models.BooleanField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating', null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='rating', null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='rating', null=True)

    def get_vote(self):
        if self.exists():
            if self.up_vote:
                return 1
            elif self.down_vote:
                return -1
        return 0

    def get_user(self):
        return self.user

    def __str__(self):
        return str(self.up_vote)
