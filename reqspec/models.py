from django.contrib.auth.models import AbstractUser, User
from django.db import models


# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#


# level 1
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=255)


# level 2
class Project(models.Model):
    client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


# level 3
class Staff(models.Model):
    role = models.CharField(max_length=255)
    # actors = models.ManyToManyField('Actor', related_name='staff')


class Actor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='actors')
    name = models.CharField(max_length=255)
    staff = models.ManyToManyField('Staff', related_name='actors')


# level 4
class UserStory(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='user_stories')
    story = models.CharField(max_length=255)


class UseCase(models.Model):
    user_stories = models.ManyToManyField(UserStory, related_name='use_cases')
    title = models.CharField(max_length=255)
    specification = models.OneToOneField('UseCaseSpecification', on_delete=models.DO_NOTHING, related_name='use_case', null=True, blank=True)


class UseCaseSpecification(models.Model):
    pass


class SpecificationSection(models.Model):
    specification = models.ForeignKey(UseCaseSpecification, on_delete=models.CASCADE, related_name='sections', null=True, blank=True)
    parent_section = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_sections', null=True, blank=True)
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)



