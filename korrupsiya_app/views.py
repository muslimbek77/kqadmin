import logging

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, ListCreateAPIView
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Korrupsiya, KarrupsiyaMalumot, KorrupsiyaFile, Vacancy, Murojaat
from .serializers import (
    KorrupsiyaSerializer,
    KarrupsiyaMalumotSerializer,
    KorrupsiyaFileSerializer,
    VacancySerializer,
    MurojaatSerializer,
    MurojaatStatusUpdateSerializer,
)
from .telegram import handle_telegram_callback, send_murojaat_to_telegram
# Create your views here.

logger = logging.getLogger(__name__)


class KorrupsiyaCreateView(CreateAPIView):
    queryset = Korrupsiya.objects.all()
    serializer_class = KorrupsiyaSerializer
  
class KorrupsiyaUpdateView(UpdateAPIView):
    queryset = Korrupsiya.objects.all()
    serializer_class = KorrupsiyaSerializer
    lookup_field = 'pk'
  
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


@method_decorator(csrf_exempt, name="dispatch")
class MurojaatListCreateAPIView(ListCreateAPIView):
    queryset = Murojaat.objects.all()
    serializer_class = MurojaatSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["phone_number", "address", "content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        instance = Murojaat.objects.get(pk=response.data["id"])
        try:
            send_murojaat_to_telegram(instance)
        except Exception:
            logger.exception("Unexpected Telegram error while creating murojaat %s", instance.pk)
        response.data = self.get_serializer(instance).data
        return response


class MurojaatDetailAPIView(RetrieveAPIView):
    queryset = Murojaat.objects.all()
    serializer_class = MurojaatSerializer


class MurojaatStatusUpdateAPIView(UpdateAPIView):
    queryset = Murojaat.objects.all()
    serializer_class = MurojaatStatusUpdateSerializer
    http_method_names = ["patch"]


class MurojaatStatisticsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Murojaat.objects.all()
        status_counts = {
            item["status"]: item["count"]
            for item in queryset.values("status").annotate(count=Count("id"))
        }
        return Response(
            {
                "total": queryset.count(),
                "new": status_counts.get(Murojaat.Status.NEW, 0),
                "tushuntirildi": status_counts.get(Murojaat.Status.TUSHUNTIRILDI, 0),
                "qoniqtirildi": status_counts.get(Murojaat.Status.QONIQTIRILDI, 0),
                "rad_etildi": status_counts.get(Murojaat.Status.RAD_ETILDI, 0),
            }
        )


@method_decorator(csrf_exempt, name="dispatch")
class TelegramWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        callback_query = request.data.get("callback_query")
        if callback_query:
            handle_telegram_callback(callback_query)
            return Response({"ok": True})
        return Response({"ok": True})
