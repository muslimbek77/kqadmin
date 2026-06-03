from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Korrupsiya, KarrupsiyaMalumot, KorrupsiyaFile, Vacancy
from .serializers import KorrupsiyaSerializer, KarrupsiyaMalumotSerializer, KorrupsiyaFileSerializer, VacancySerializer
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_seen_count()
        return super().retrieve(request, *args, **kwargs)


class KorrupsiyaFileListView(ListAPIView):
    queryset = KorrupsiyaFile.objects.all()
    serializer_class = KorrupsiyaFileSerializer


class VacancyListAPIView(ListAPIView):
    queryset = Vacancy.objects.all().order_by('-published_date')
    serializer_class = VacancySerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'type', 'status', 'location']
    search_fields = ['title', 'company', 'responsibilities', 'requirements']
    ordering_fields = ['published_date', 'deadline', 'salary', 'created_at']
    ordering = ['-published_date']


class VacancyDetailAPIView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer