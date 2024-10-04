from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Prefetch


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('The user must have an email')

        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None):
        if username == "":
            username = None
        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, null=True, blank=True, max_length=300, verbose_name='Username')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_admin = models.BooleanField(default=False, verbose_name='Admin')
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username or self.email

    @property
    def is_staff(self):
        return self.is_admin

    @classmethod
    def get_users_with_groups(cls):
        return cls.objects.filter(is_admin=False).prefetch_related(
            Prefetch(
                'membership_set',
                queryset=Membership.objects.select_related('group')
            )
        )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Group(models.Model):
    name = models.CharField(unique=True, null=True, blank=True, max_length=300, verbose_name='Name')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    @classmethod
    def get_groups_with_users(cls):
        return cls.objects.prefetch_related(
            Prefetch(
                'membership_set',
                queryset=Membership.objects.select_related('user')
            )
        )

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.username} in {self.group.name} since {self.date_added}"

