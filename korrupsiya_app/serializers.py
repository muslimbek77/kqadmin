from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Korrupsiya, KarrupsiyaMalumot, KorrupsiyaFile, Vacancy, Murojaat


class KorrupsiyaSerializer(ModelSerializer):
    class Meta:
        model = Korrupsiya
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
class KarrupsiyaMalumotSerializer(ModelSerializer):
    class Meta:
        model = KarrupsiyaMalumot
        fields = '__all__'
    
class KorrupsiyaFileSerializer(ModelSerializer):
    class Meta:
        model = KorrupsiyaFile
        fields = '__all__'


class VacancySerializer(ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MurojaatSerializer(ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Murojaat
        fields = [
            "id",
            "phone_number",
            "address",
            "content",
            "attachment",
            "status",
            "status_display",
            "assigned_telegram_chat_id",
            "telegram_sent_at",
            "telegram_error",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "status",
            "status_display",
            "telegram_sent_at",
            "telegram_error",
            "created_at",
            "updated_at",
        ]


class MurojaatStatusUpdateSerializer(ModelSerializer):
    class Meta:
        model = Murojaat
        fields = ["status"]
