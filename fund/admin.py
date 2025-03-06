from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
	add_form = UserCreationForm
	# form = UserChangeForm
	model = User

	fieldsets = (
		(None, {"fields": ("username", "email", "password")}),
		(_("Personal info"), {"fields": ("first_name", "last_name", "mobile_phone", "profile_picture")}),
		(_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
		(_("Important dates"), {"fields": ("last_login", "date_joined")}),
	)

	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": ("username", "email", "password1", "password2"),
		}),
	)

	list_display = ("email", "username", "first_name", "last_name", "is_staff", "created_at")
	search_fields = ("email", "username", "first_name", "last_name")
	ordering = ("email",)


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 3


class AdminProjectForm(admin.ModelAdmin):
	inlines = [PictureInline]


admin.site.register(Project, AdminProjectForm)
admin.site.register(Picture)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Rate)
admin.site.register(Reply)
admin.site.register(Report)
admin.site.register(Tag)
admin.site.register(Donation)
admin.site.register(Token)
