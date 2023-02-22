#############
# LIBRARIES #
#############
from django.contrib import admin
from django.urls import path, include
from authentication.views import UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from projects.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet


#############
# VARIABLES #
#############
router = routers.DefaultRouter()
router.register(r"", ProjectViewSet, basename="projects")
router.register(r"^(?P<project_id>[^/.]+)/users", ContributorViewSet, basename="users")
router.register(r"^(?P<project_id>[^/.]+)/issues", IssueViewSet, basename="issues")
router.register(r"^(?P<project_id>[^/.]+)/issues/(?P<issue_id>[^/.]+)/comments", CommentViewSet, basename="comments")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refresh/token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/', include(router.urls)),
]
