from django.contrib import admin
from .models import Korrupsiya, KarrupsiyaMalumot, KorrupsiyaFile, Vacancy, Murojaat
# Register your models here.
admin.site.register(Korrupsiya)
admin.site.register(KarrupsiyaMalumot)
admin.site.register(KorrupsiyaFile)


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
        "assigned_telegram_chat_id",
        "telegram_sent_at",
        "created_at",
    )
    list_filter = ("status", "created_at", "telegram_sent_at")
    search_fields = ("phone_number", "address", "content")
    readonly_fields = ("telegram_sent_at", "telegram_error", "created_at", "updated_at")
