from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    UserSerializer,
    UserWithGroupsSerializer,
    UserCreateUpdateSerializer,
    GroupsWithUserSerializer,
    GroupCreateUpdateSerializer,
    BulkMembershipSerializer
)
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User, Group, Membership


# start of Group Api region
class ListGroupView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = GroupsWithUserSerializer
    queryset = Group.get_groups_with_users()


class CreateGroupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = GroupCreateUpdateSerializer


class RetrieveDestroyGroupView(generics.RetrieveDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = GroupsWithUserSerializer
    queryset = Group.get_groups_with_users()


class UpdateGroupView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = GroupCreateUpdateSerializer
    queryset = Group.get_groups_with_users()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(GroupsWithUserSerializer(instance).data)

# end of Group Api region


# start of User Api region
class UserListView(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = UserWithGroupsSerializer
    queryset = User.get_users_with_groups()


class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateUpdateSerializer


class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserWithGroupsSerializer
    queryset = User.get_users_with_groups()


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateUpdateSerializer
    queryset = User.get_users_with_groups()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(UserWithGroupsSerializer(instance).data)


class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
# end of User Api region


class MembershipBulkView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = BulkMembershipSerializer

    @swagger_auto_schema(
        operation_description="Request for bulk update of users to groups",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                    'group_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Group ID'),
                    'action': openapi.Schema(type=openapi.TYPE_STRING,
                                             description='Action to perform (e.g., add, remove)')
                },
                example={
                    "user_id": 3,
                    "group_id": 1,
                    "action": "add"
                }
            ),
        ),
        responses={200: "Success"}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            user_ids = User.objects.filter(is_admin=False).values_list(flat=True)
            group_ids = Group.objects.all()
            for item in serializer.validated_data:
                user_id = item['user_id']
                group_id = item['group_id']
                action = item['action']

                if user_id not in user_ids or group_id not in group_ids:
                    continue

                if action == 'add':
                    Membership.objects.get_or_create(user_id=user_id, group_id=group_id)
                elif action == 'remove':
                    Membership.objects.filter(user_id=user_id, group_id=group_id).delete()

            return Response({"detail": "Users updated successfully."}, status=status.HTTP_200_OK)
