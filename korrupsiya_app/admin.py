from django.contrib import admin
from .models import Korrupsiya, KarrupsiyaMalumot, KorrupsiyaFile, Vacancy
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
