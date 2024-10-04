from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from comments.views import CommentsAPI, EditCommentAPI
from accounts.views import (
    UserRegisterView,
    UserListView,
    UserCreateView,
    UserRetrieveDestroyView,
    UserUpdateView,
    CreateGroupView,
    UpdateGroupView,
    RetrieveDestroyGroupView,
    ListGroupView,
    MembershipBulkView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test MB Digital project description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

doc_urls = [
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

token_urls = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


user_urls = [
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/create-new/", UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/", UserRetrieveDestroyView.as_view(), name="user_retrieve_delete"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
]


group_urls = [
    path("groups/", ListGroupView.as_view(), name="group_list"),
    path("groups/create-new/", CreateGroupView.as_view(), name="group_create"),
    path("groups/<int:pk>/", RetrieveDestroyGroupView.as_view(), name="group_retrieve_delete"),
    path("groups/<int:pk>/update/", UpdateGroupView.as_view(), name="group_update"),
]

membership_urls = [
    path("membership-change/", MembershipBulkView.as_view(), name="membership-change"),
]

auth_urls = [
     path("auth/register/", UserRegisterView.as_view(), name="register"),
     path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
     path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/", include(doc_urls + auth_urls + user_urls + group_urls + membership_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
