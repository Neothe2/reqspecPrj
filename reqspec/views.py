from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Client, Project, Actor, UserStory, UseCase, UseCaseSpecification, SpecificationSection, Staff
from .serializers import ClientSerializer, ProjectSerializer, ActorSerializer, UserStorySerializer, UseCaseSerializer, \
    UseCaseSpecificationSerializer, SpecificationSectionSerializer, StaffSerializer, EditStaffSerializer, \
    EditActorSerializer, EditUserStorySerializer, EditUseCaseSerializer, AddActorSerializer, CreateStaffSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name']
    filterset_fields = {'name': ['iexact', 'icontains']}
    ordering_fields = ['name']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    # TODO: Add a perform create method and find the value of client id and make that the client attr of the project obj
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'client__name']
    filterset_fields = {'title': ['iexact', 'icontains'], 'client__name': ['iexact', 'icontains']}
    ordering_fields = ['title', 'client__name']

    def get_queryset(self):
        return Project.objects.filter(client_id=self.kwargs['client_pk'], client__user=self.request.user)


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['role', 'project__title']
    filterset_fields = {'role': ['iexact', 'icontains'], 'project__title': ['iexact', 'icontains']}
    ordering_fields = ['role', 'project__title']

    def get_queryset(self):
        return Actor.objects.filter(project_id=self.kwargs['project_pk'], project__client__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return EditActorSerializer
        elif self.request.method == 'POST':
            return AddActorSerializer
        return ActorSerializer

    @action(detail=True, methods=['GET'])
    def unassociated_staff(self, request, project_pk=None, pk=None, client_pk=None):
        actor = self.get_object()
        all_staff_in_project = Staff.objects.filter(project_id=project_pk)
        associated_staff = actor.staff.all()

        unassociated_staff = all_staff_in_project.exclude(id__in=associated_staff.values_list('id', flat=True))

        # Serialize the queryset
        serializer = StaffSerializer(unassociated_staff, many=True)

        return Response(serializer.data)


class StaffViewSet(viewsets.ModelViewSet):
    # serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'actors__role']
    filterset_fields = {'name': ['iexact', 'icontains'], 'actors__role': ['iexact', 'icontains']}
    ordering_fields = ['name', 'actors__role']

    def get_queryset(self):
        return Staff.objects.filter(project__id=self.kwargs['project_pk'], project__client__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return EditStaffSerializer
        elif self.request.method == 'POST':
            return CreateStaffSerializer
        return StaffSerializer

    @action(detail=True, methods=['GET'])
    def unassociated_actors(self, request, client_pk=None, project_pk=None, pk=None):
        staff = self.get_object()
        all_actors_in_project = Actor.objects.filter(project__id=project_pk)
        associated_actors = staff.actors.all()

        unassociated_actors = all_actors_in_project.exclude(id__in=associated_actors.values_list('id', flat=True))

        # Serialize the queryset
        serializer = ActorSerializer(unassociated_actors, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def associated_actors(self, request, pk=None, client_pk=None, project_pk=None):
        staff_instance = self.get_object()
        associated_actors = Actor.objects.filter(staff=staff_instance)
        serializer = ActorSerializer(associated_actors, many=True)
        return Response(serializer.data)


class UserStoryViewSet(viewsets.ModelViewSet):
    serializer_class = UserStorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['story', 'actor__role']
    filterset_fields = {'story': ['iexact', 'icontains'], 'actor__role': ['iexact', 'icontains']}
    ordering_fields = ['story', 'actor__role']

    def get_queryset(self):
        return UserStory.objects.filter(actor_id=self.kwargs['actor_pk'],
                                        actor__project__client__user=self.request.user)
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return EditUserStorySerializer
        return UserStorySerializer

    @action(detail=True, methods=['GET'])
    def get_unassociated_use_cases(self, request, client_pk=None, project_pk=None, actor_pk=None, pk=None):
        user_story = self.get_object()
        all_use_cases_in_project = UseCase.objects.filter(actor__project__id=project_pk)
        associated_use_cases = user_story.use_cases.all()

        unassociated_use_cases = all_use_cases_in_project.exclude(id__in=associated_use_cases.values_list('id', flat=True))

        # Serialize the queryset
        serializer = UseCaseSerializer(unassociated_use_cases, many=True)

        return Response(serializer.data)


class UseCaseViewSet(viewsets.ModelViewSet):
    serializer_class = UseCaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'user_stories__story']
    filterset_fields = {'title': ['iexact', 'icontains'], 'user_stories__story': ['iexact', 'icontains']}
    ordering_fields = ['title', 'user_stories__story']

    def get_queryset(self):
        return UseCase.objects.filter(actor__id=self.kwargs['actor_pk'])

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return EditUseCaseSerializer
        return UseCaseSerializer

    @action(detail=True, methods=['GET'])
    def get_unassociated_user_stories(self, request, client_pk=None, project_pk=None, actor_pk=None, pk=None):
        use_case = self.get_object()
        all_user_stories_in_project = UserStory.objects.filter(actor__project__id=project_pk)
        associated_user_stories = use_case.user_stories.all()

        unassociated_user_stories = all_user_stories_in_project.exclude(id__in=associated_user_stories.values_list('id', flat=True))

        # Serialize the queryset
        serializer = UserStorySerializer(unassociated_user_stories, many=True)

        return Response(serializer.data)


class UseCaseSpecificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UseCaseSpecificationSerializer

    def get_queryset(self):
        return UseCaseSpecification.objects.filter(use_case=self.kwargs['usecase_pk'],
                                                   )


class SpecificationSectionViewSet(viewsets.ModelViewSet):
    serializer_class = SpecificationSectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['body', 'specification__id']
    filterset_fields = {
        'body': ['iexact', 'icontains'],
        'specification__id': ['iexact', 'icontains'],
    }
    ordering_fields = ['body', 'specification__id']

    def get_queryset(self):
        return SpecificationSection.objects.filter(specification_id=self.kwargs.get('usecasespecification_pk'),
                                                   )
