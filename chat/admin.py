from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from chat.models import Profile, Message

# Inline Profile admin to edit Profile alongside User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('profile_picture', 'status')
    list_display = ('profile_picture', 'status')

# Custom User admin to include Profile inline
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_status')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'profile__status')
    
    def get_status(self, obj):
        return obj.profile.status
    get_status.short_description = 'Status'

# Message admin
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content_preview', 'timestamp', 'read')
    list_filter = ('timestamp', 'read', 'sender', 'recipient')
    search_fields = ('sender__username', 'recipient__username', 'content')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content'

# Register models
admin.site.unregister(User)
admin.site.register(User, UserAdmin)