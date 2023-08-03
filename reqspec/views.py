from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Client, Project, Actor, UserStory, UseCase, UseCaseSpecification, SpecificationSection, Staff
from .serializers import ClientSerializer, ProjectSerializer, ActorSerializer, UserStorySerializer, UseCaseSerializer, UseCaseSpecificationSerializer, SpecificationSectionSerializer, StaffSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name']
    filterset_fields = {'name': ['iexact', 'icontains']}
    ordering_fields = ['name']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'client__name']
    filterset_fields = {'title': ['iexact', 'icontains'], 'client__name': ['iexact', 'icontains']}
    ordering_fields = ['title', 'client__name']

    def get_queryset(self):
        return Project.objects.filter(client_id=self.kwargs['client_pk'])


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'project__title']
    filterset_fields = {'name': ['iexact', 'icontains'], 'project__title': ['iexact', 'icontains']}
    ordering_fields = ['name', 'project__title']

    def get_queryset(self):
        return Actor.objects.filter(project_id=self.kwargs['project_pk'])


class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['role', 'actors__name']
    filterset_fields = {'role': ['iexact', 'icontains'], 'actors__name': ['iexact', 'icontains']}
    ordering_fields = ['role', 'actors__name']

    def get_queryset(self):
        return Staff.objects.filter(actors__id=self.kwargs['actor_pk'])


class UserStoryViewSet(viewsets.ModelViewSet):
    serializer_class = UserStorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['story', 'actor__name']
    filterset_fields = {'story': ['iexact', 'icontains'], 'actor__name': ['iexact', 'icontains']}
    ordering_fields = ['story', 'actor__name']

    def get_queryset(self):
        return UserStory.objects.filter(actor_id=self.kwargs['actor_pk'])


class UseCaseViewSet(viewsets.ModelViewSet):
    serializer_class = UseCaseSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'user_stories__story']
    filterset_fields = {'title': ['iexact', 'icontains'], 'user_stories__story': ['iexact', 'icontains']}
    ordering_fields = ['title', 'user_stories__story']

    def get_queryset(self):
        return UseCase.objects.filter(user_stories__id=self.kwargs['user_story_pk'])


class UseCaseSpecificationViewSet(viewsets.ModelViewSet):
    serializer_class = UseCaseSpecificationSerializer

    def get_queryset(self):
        return UseCaseSpecification.objects.filter(use_case_id=self.kwargs['use_case_pk'])


class SpecificationSectionViewSet(viewsets.ModelViewSet):
    serializer_class = SpecificationSectionSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'body', 'specification__id', 'parent_section__title']
    filterset_fields = {
        'title': ['iexact', 'icontains'],
        'body': ['iexact', 'icontains'],
        'specification__id': ['iexact', 'icontains'],
        'parent_section__title': ['iexact', 'icontains']
    }
    ordering_fields = ['title', 'body', 'specification__id', 'parent_section__title']

    def get_queryset(self):
        return SpecificationSection.objects.filter(specification_id=self.kwargs['use_case_specification_pk'])
