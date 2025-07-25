from rest_framework.serializers import ModelSerializer
from .models import Korrupsiya,KarrupsiyaMalumot,KorrupsiyaFile


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