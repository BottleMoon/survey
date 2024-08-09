from django.db import models

from user.models import User


# Create your models here.
class Classification(models.Model):
    text = models.TextField()


class Survey(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    small_description = models.TextField()
    main_description = models.TextField()


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()


class ChoiceUser(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Target(models.Model):
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE, null=True)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    sex = models.CharField(max_length=1)
    job = models.TextField()


class TargetExtra(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField()


class TargetExtraUser(models.Model):
    targetExtra = models.ForeignKey(TargetExtra, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)