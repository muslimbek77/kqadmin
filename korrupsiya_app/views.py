from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView,RetrieveAPIView
from .models import Korrupsiya,KarrupsiyaMalumot, KorrupsiyaFile    
from .serializers import KorrupsiyaSerializer, KarrupsiyaMalumotSerializer, KorrupsiyaFileSerializer
# Create your views here.


class KorrupsiyaCreateView(CreateAPIView):
    queryset = Korrupsiya.objects.all()
    serializer_class = KorrupsiyaSerializer
  
class KarrupsiyaMalumotListView(ListAPIView):
    queryset = KarrupsiyaMalumot.objects.all()
    serializer_class = KarrupsiyaMalumotSerializer

class KorrupsiyaMalumotDetailView(RetrieveAPIView):
    queryset = KarrupsiyaMalumot.objects.all()
    serializer_class = KarrupsiyaMalumotSerializer

class KorrupsiyaFileListView(ListAPIView):
    queryset = KorrupsiyaFile.objects.all()
    serializer_class = KorrupsiyaFileSerializer