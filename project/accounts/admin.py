from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as DefaultGroup

from rest_framework.authtoken.models import Token

from .forms import UserChangeForm, UserCreationForm
from .models import User, Group, Membership


class ForUserMembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    fields = ['group', 'date_added']
    raw_id_fields = ['group']
    readonly_fields = ['date_added']


class ForGroupMembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    fields = ['user', 'date_added']
    raw_id_fields = ['user']
    readonly_fields = ['date_added']


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name', 'id')
    inlines = (ForGroupMembershipInline,)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_admin', 'is_active',)
    list_filter = ('is_admin', 'is_admin',)
    search_fields = ('username', 'id', 'email')
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'password',
                ('is_admin', 'is_active', 'is_superuser',),
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password_confirmation')}
         ),
    )
    ordering = ('-id',)
    filter_horizontal = ()
    inlines = (ForUserMembershipInline,)


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.unregister(DefaultGroup)

