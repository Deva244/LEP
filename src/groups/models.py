from django.db import models
import random
from django.contrib.auth import get_user_model

# Create your models here.

user = get_user_model()

def code_generator():
    return random.randint(100000, 999999)

def user_full_name():
    return user.get_full_name

def user_email():
    return user.get_email

class Group(models.Model):
    group_name   = models.CharField(max_length=50, unique=True)
    group_code   = models.IntegerField(default=code_generator, unique=True)
    group_owner  = models.CharField(default="manager", max_length=255)
    member_count = models.IntegerField(default=0)

    def __str__(self):
        return self.group_name

class Manager(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    name  = models.CharField(default=user_full_name, max_length=255)
    email = models.CharField(default=user_email, max_length=255)

    def __str__(self):
        return self.email

class GroupJoin(models.Model):
    group_code  = models.IntegerField()

class Teacher(models.Model):
    groups          = models.ManyToManyField(Group)
    group_owner     = models.ManyToManyField(Manager)
    teacher_name    = models.CharField(default=user_full_name, max_length=255)
    teacher_email   = models.CharField(default=user_email, max_length=255)
    exam_perm       = models.BooleanField(default=False)

    def __str__(self):
        return self.teacher_email

class Student(models.Model):
    group           = models.ForeignKey(Group, on_delete=models.CASCADE)
    group_owner     = models.ForeignKey(Manager, on_delete=models.CASCADE, default='owner')
    student_name    = models.CharField(default=user_full_name, max_length=255)
    student_email   = models.CharField(default=user_email, max_length=255)

    def __str__(self):
        return self.student_email
