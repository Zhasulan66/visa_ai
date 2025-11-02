from django.contrib import admin
from .models import User, Chat, Subscription, EsimOrder, Consultant, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "iin", "phone", "verified", "role")
    search_fields = ("iin", "phone")
    list_filter = ("verified", "role")


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type")
    search_fields = ("user__phone",)
    list_filter = ("type",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "start_date", "end_date")
    search_fields = ("user__phone",)
    list_filter = ("status",)


@admin.register(EsimOrder)
class EsimOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "country", "plan_id", "status")
    search_fields = ("user__phone", "country")
    list_filter = ("status",)


@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    filter_horizontal = ("assigned_users",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "sender", "content", "created_at")
    search_fields = ("chat__user__username", "sender", "content")
    list_filter = ("sender",)
