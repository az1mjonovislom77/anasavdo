from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from app.user.models import User, VerificationOTP


@admin.register(User)
class UserAdmin(BaseUserAdmin, UnfoldModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("full_name", "phone_number", "role", "auth_type", "image")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "full_name", "phone_number", "role", "is_active")
    list_filter = ("is_active", "role")


@admin.register(VerificationOTP)
class VerificationAdmin(UnfoldModelAdmin):
    list_display = ('user', 'is_confirmed', 'auth_type', 'expires_time')
    list_filter = ('user', 'is_confirmed', 'auth_type')
    search_fields = ('user',)

