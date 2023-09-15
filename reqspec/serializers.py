from rest_framework import serializers
from .models import Client, Project, Actor, UserStory, UseCase, UseCaseSpecification, SpecificationSection, Staff


class SpecificationSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationSection
        fields = ['id', 'specification', 'body']


class UseCaseSpecificationSerializer(serializers.ModelSerializer):
    sections = SpecificationSectionSerializer(many=True, read_only=True)

    class Meta:
        model = UseCaseSpecification
        fields = ['id', 'sections', 'use_case']


class UserStorySerializer(serializers.ModelSerializer):
    use_cases = serializers.PrimaryKeyRelatedField(many=True, queryset=UseCase.objects.all(), required=False)

    class Meta:
        model = UserStory
        fields = ['id', 'actor', 'story', 'use_cases']


class UseCaseSerializer(serializers.ModelSerializer):
    user_stories = UserStorySerializer(many=True, read_only=True)
    specification = UseCaseSpecificationSerializer(read_only=True)

    class Meta:
        model = UseCase
        fields = ['id', 'user_stories', 'title', 'specification', 'actor']


class EditUserStorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStory
        fields = ['id', 'actor', 'story', 'use_cases']


class EditUseCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UseCase
        fields = ['id', 'user_stories', 'title', 'actor']


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ['id', 'name', 'actors', 'project']


class CreateStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'project']


class ActorSerializer(serializers.ModelSerializer):
    user_stories = UserStorySerializer(many=True, read_only=True)
    staff = StaffSerializer(many=True, read_only=True, required=False)
    use_cases = UseCaseSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Actor
        fields = ['id', 'project', 'role', 'user_stories', 'staff', 'use_cases']


class EditStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'actors', 'project']


class AddActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'project', 'role']


class EditActorSerializer(serializers.ModelSerializer):
    staff = serializers.PrimaryKeyRelatedField(many=True, queryset=Staff.objects.all(), required=False)
    class Meta:
        model = Actor
        fields = ['id', 'project', 'role', 'staff']


class ProjectSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    staff = StaffSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'client', 'actors', 'staff', 'title']


class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'projects']
