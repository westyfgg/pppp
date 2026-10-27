from django.contrib import admin

from .models import ContactMessage, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "tech_stack", "is_published", "order", "created_at")
    list_filter = ("is_published", "created_at")
    list_editable = ("is_published", "order")
    search_fields = ("title", "description", "tech_stack")
    readonly_fields = ("created_at",)
    ordering = ("order", "-created_at")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "telegram", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "telegram", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
