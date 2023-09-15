from django.urls import path
from rest_framework_nested import routers
from .views import (
    ClientViewSet,
    ProjectViewSet,
    ActorViewSet,
    UserStoryViewSet,
    UseCaseViewSet,
    UseCaseSpecificationViewSet,
    SpecificationSectionViewSet,
    StaffViewSet,
)

router = routers.SimpleRouter()

router.register(r'clients', ClientViewSet, basename='clients')

clients_router = routers.NestedSimpleRouter(router, r'clients', lookup='client')
clients_router.register(r'projects', ProjectViewSet, basename='client-projects')

projects_router = routers.NestedSimpleRouter(clients_router, r'projects', lookup='project')
projects_router.register(r'actors', ActorViewSet, basename='project-actors')
projects_router.register(r'staff', StaffViewSet, basename='project-staff')  # Now parallel to actors
projects_router.urls.append(
    path('staff/<int:pk>/unassociated_actors/', StaffViewSet.as_view({'get': 'unassociated_actors'}), name='staff-unassociated-actors')
)
projects_router.urls.append(
    path('staff/<int:pk>/associated_actors/', StaffViewSet.as_view({'get': 'associated_actors'}), name='staff-actors')
)

actors_router = routers.NestedSimpleRouter(projects_router, r'actors', lookup='actor')
actors_router.register(r'user_stories', UserStoryViewSet, basename='actor-userstories')
actors_router.register(r'use_cases', UseCaseViewSet, basename='actor-usecases')  # Now parallel to user_stories
actors_router.urls.append(
    path('<int:pk>/unassociated_staff/', ActorViewSet.as_view({'get': 'unassociated_staff'}), name='actor-unassociated-staff')
)
actors_router.urls.append(
    path('user_stories/<int:pk>/get_unassociated_use_cases/', UserStoryViewSet.as_view({'get': 'get_unassociated_use_cases'}), name='user_story-unassociated-use_cases')
)

# If you need nested routes under use_cases for their specifications, you can still use the routers below. Otherwise,
# you can comment or remove them.
use_cases_router = routers.NestedSimpleRouter(actors_router, r'use_cases', lookup='usecase')
use_cases_router.register(r'use_case_specifications', UseCaseSpecificationViewSet, basename='usecase-usecasespecifications')
use_cases_router.urls.append(
    path('<int:usecase_pk>/unassociated_user_stories/', UseCaseViewSet.as_view({'get': 'get_unassociated_user_stories'}), name='usecase-unassociated-user_stories')
)


use_case_specifications_router = routers.NestedSimpleRouter(use_cases_router, r'use_case_specifications', lookup='usecasespecification')
use_case_specifications_router.register(r'specification_sections', SpecificationSectionViewSet, basename='usecasespecification-specificationsections')

urlpatterns = []
urlpatterns += router.urls
urlpatterns += clients_router.urls
urlpatterns += projects_router.urls
urlpatterns += actors_router.urls
urlpatterns += use_cases_router.urls
urlpatterns += use_case_specifications_router.urls
