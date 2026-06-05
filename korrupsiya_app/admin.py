from django.contrib import admin
from .models import (
    Korrupsiya,
    KarrupsiyaMalumot,
    KorrupsiyaFile,
    Vacancy,
    TelegramSettings,
    Murojaat,
)
# Register your models here.
admin.site.register(Korrupsiya)
admin.site.register(KarrupsiyaMalumot)
admin.site.register(KorrupsiyaFile)


@admin.register(TelegramSettings)
class TelegramSettingsAdmin(admin.ModelAdmin):
    list_display = ("masked_bot_token", "admin_chat_id", "updated_at")
    search_fields = ("admin_chat_id",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Telegram Sozlamalari",
            {
                "fields": ("bot_token", "admin_chat_id", "created_at", "updated_at"),
            },
        ),
    )

    def has_add_permission(self, request):
        return not TelegramSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Bot token")
    def masked_bot_token(self, obj):
        if not obj.bot_token:
            return ""
        if len(obj.bot_token) <= 8:
            return "*" * len(obj.bot_token)
        return f"{obj.bot_token[:4]}...{obj.bot_token[-4:]}"


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('company', 'title', 'status', 'published_date', 'deadline')
    list_filter = ('status', 'published_date', 'type')
    search_fields = ('company', 'title')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Asosiy Ma\'lumot', {
            'fields': ('company', 'title', 'status')
        }),
        ('Ish Shartlari', {
            'fields': ('type', 'work_hours', 'location', 'salary', 'experience', 'education')
        }),
        ('Tariflar', {
            'fields': ('responsibilities', 'requirements', 'languages', 'conditions', 'positions')
        }),
        ('Tillar', {
            'fields': ('title_translations', 'description_translations'),
            'classes': ('collapse',)
        }),
        ('Qo\'shimcha', {
            'fields': ('extra',),
            'classes': ('collapse',)
        }),
        ('Sana', {
            'fields': ('published_date', 'deadline', 'created_at', 'updated_at')
        }),
    )


@admin.register(Murojaat)
class MurojaatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone_number",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("phone_number", "address", "content")
    readonly_fields = ("created_at", "updated_at")
