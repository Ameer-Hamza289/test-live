from django.contrib import admin
from .models import CallSession, Conversation, CallFeedback

# Register your models here.
admin.site.register(CallSession)
admin.site.register(Conversation)

@admin.register(CallFeedback)
class CallFeedbackAdmin(admin.ModelAdmin):
    list_display = ['session', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['session__session_id', 'comments']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
