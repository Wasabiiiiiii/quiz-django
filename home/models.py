from django.db import models
from django.contrib.auth.models import User
import random
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Quiz(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    content = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Answer(models.Model):
    content = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.content}, answer: {self.content}, correct: {self.correct}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class UserQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz.name
