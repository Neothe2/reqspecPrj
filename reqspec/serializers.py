from rest_framework import serializers
from .models import Client, Project, Actor, UserStory, UseCase, UseCaseSpecification, SpecificationSection, Staff


class SpecificationSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationSection
        fields = ['id', 'specification', 'parent_section', 'title', 'body']


class UseCaseSpecificationSerializer(serializers.ModelSerializer):
    sections = SpecificationSectionSerializer(many=True, read_only=True)

    class Meta:
        model = UseCaseSpecification
        fields = ['id', 'sections']


class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStory
        fields = ['id', 'actor', 'story']


class UseCaseSerializer(serializers.ModelSerializer):
    user_stories = UserStorySerializer(many=True)
    specification = UseCaseSpecificationSerializer()

    class Meta:
        model = UseCase
        fields = ['id', 'user_stories', 'title', 'specification']


class StaffSerializer(serializers.ModelSerializer):
    # actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Staff
        fields = ['id', 'role', 'actors']

class ActorSerializer(serializers.ModelSerializer):
    user_stories = UserStorySerializer(many=True, read_only=True)
    staff = StaffSerializer(many=True, read_only=True)


    class Meta:
        model = Actor
        fields = ['id', 'project', 'name', 'user_stories', 'staff']





class CreateStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ['id', 'role', 'actors']





class ProjectSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'client', 'actors', 'title']


class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'projects']
