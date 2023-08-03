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

actors_router = routers.NestedSimpleRouter(projects_router, r'actors', lookup='actor')
actors_router.register(r'staff', StaffViewSet, basename='actor-staff')  # new addition
actors_router.register(r'user_stories', UserStoryViewSet, basename='actor-userstories')

user_stories_router = routers.NestedSimpleRouter(actors_router, r'user_stories', lookup='userstory')
user_stories_router.register(r'use_cases', UseCaseViewSet, basename='userstory-usecases')

use_cases_router = routers.NestedSimpleRouter(user_stories_router, r'use_cases', lookup='usecase')
use_cases_router.register(r'use_case_specifications', UseCaseSpecificationViewSet, basename='usecase-usecasespecifications')

use_case_specifications_router = routers.NestedSimpleRouter(use_cases_router, r'use_case_specifications', lookup='usecasespecification')
use_case_specifications_router.register(r'specification_sections', SpecificationSectionViewSet, basename='usecasespecification-specificationsections')

urlpatterns = []
urlpatterns += router.urls
urlpatterns += clients_router.urls
urlpatterns += projects_router.urls
urlpatterns += actors_router.urls
urlpatterns += user_stories_router.urls
urlpatterns += use_cases_router.urls
urlpatterns += use_case_specifications_router.urls
