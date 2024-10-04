from rest_framework import serializers
from .models import User, Group
from django.utils import timezone


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class GroupMembershipSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    group_name = serializers.CharField(source='group.name')
    group_id = serializers.IntegerField(source='group.id')
    time_in_group = serializers.SerializerMethodField()

    def get_time_in_group(self, obj):
        time_in_group = timezone.now() - obj.date_added
        days, seconds = time_in_group.days, time_in_group.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{days} days, {hours}:{minutes:02}"


class UserWithGroupsSerializer(serializers.ModelSerializer):
    groups = GroupMembershipSerializer(many=True, source='membership_set')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class UserMembershipSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    group_id = serializers.IntegerField(source='user.id')
    time_in_group = serializers.SerializerMethodField()

    def get_time_in_group(self, obj):
        time_in_group = timezone.now() - obj.date_added
        days, seconds = time_in_group.days, time_in_group.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{days} days, {hours}:{minutes:02}"


class GroupsWithUserSerializer(serializers.ModelSerializer):
    users = UserMembershipSerializer(many=True, source='membership_set')

    class Meta:
        model = Group
        fields = ['id', 'name', 'users']


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class BulkMembershipSerializer(serializers.Serializer):


    # @swagger_auto_schema(
    #     responses={
    #         200: openapi.Response(
    #             description="A successful response with example data",
    #             examples={
    #                 "application/json": {
    #                     "name": "John Doe",
    #                     "age": 30
    #                 }
    #             }
    #         )
    #     }
    # )
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['add', 'remove'])
