from django.db import models
from django.contrib.auth.models import User


class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.TextField(max_length=10)
    license_number = models.TextField(max_length=5, null=True)
    balance = models.PositiveIntegerField()


class Course(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=20)
    price = models.PositiveIntegerField()
    # tag


class Post(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField()


class CourseStudents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class StudentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    HEALTH_CHOICES = ['sugar', 'pressure', 'height', 'weight', 'food'
                      'sleep', 'watter', 'coffee', 'tea', 'running', 'cycling', 'swimming',
                      'hiking', 'walking', 'dancing']
    HEALTH_CHOICES = [(i, item) for i, item in enumerate(HEALTH_CHOICES)]
    history_type = models.CharField(
        max_length=9, choices=HEALTH_CHOICES, default='1')
    details = models.TextField(max_length=200)
    value = models.TextField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
