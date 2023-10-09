from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, User
from core.admin import StudentSectionInline, AssistantSectionInline


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'national_id',
                    'email',
                    'first_name',
                    'last_name',
                    'description',
                    'father_name',
                    'biography',
                    'website',
                    'linkedin',
                    'telegram',
                    'entering_year',
                    'field',
                    'display_student_sections',
                    'display_assistant_sections',
                    'display_teaching_sections')
    search_fields = ('first_name', 'last_name', 'username')
    inlines = [StudentSectionInline, AssistantSectionInline, ]

    readonly_fields = ('password', )

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.national_id)
        return super(UserAdmin, self).save_model(request, obj, form, change)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', )
    search_fields = ('user__first_name', 'user__last_name', )
    list_filter = ('group', )


class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('name', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Permission, PermissionAdmin)
