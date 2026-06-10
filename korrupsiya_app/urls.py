from django.urls import path
from .views import (
    KorrupsiyaCreateView, KorrupsiyaUpdateView, KarrupsiyaMalumotListView, KorrupsiyaMalumotDetailView,
    KorrupsiyaMalumotUpdateView, KorrupsiyaFileListView, KorrupsiyaFileUpdateView, VacancyListAPIView, VacancyDetailAPIView,
    MurojaatListCreateAPIView, MurojaatDetailAPIView, MurojaatStatusUpdateAPIView,
    MurojaatStatisticsAPIView, TelegramWebhookAPIView,
)

urlpatterns = [
    path('korrupsiya/', KorrupsiyaCreateView.as_view(), name='korrupsiya-create'),
    path('korrupsiya/<int:pk>/', KorrupsiyaUpdateView.as_view(), name='korrupsiya-update'),
    path('karrupsiya-malumot/', KarrupsiyaMalumotListView.as_view(), name='karrupsiya-malumot-list'),
    path('karrupsiya-malumot/<int:pk>/', KorrupsiyaMalumotDetailView.as_view(), name='karrupsiya-malumot-detail'),
    path('karrupsiya-malumot/<int:pk>/update/', KorrupsiyaMalumotUpdateView.as_view(), name='karrupsiya-malumot-update'),
    path('korrupsiya-file/', KorrupsiyaFileListView.as_view(), name='korrupsiya-file-list'),
    path('korrupsiya-file/<int:pk>/update/', KorrupsiyaFileUpdateView.as_view(), name='korrupsiya-file-update'),
    path('vacancies/', VacancyListAPIView.as_view(), name='vacancy-list'),
    path('vacancies/<int:pk>/', VacancyDetailAPIView.as_view(), name='vacancy-detail'),
    path('murojaatlar', MurojaatListCreateAPIView.as_view()),
    path('murojaatlar/', MurojaatListCreateAPIView.as_view(), name='murojaat-list-create'),
    path('murojaatlar/statistics', MurojaatStatisticsAPIView.as_view()),
    path('murojaatlar/statistics/', MurojaatStatisticsAPIView.as_view(), name='murojaat-statistics'),
    path('murojaatlar/<int:pk>', MurojaatDetailAPIView.as_view()),
    path('murojaatlar/<int:pk>/', MurojaatDetailAPIView.as_view(), name='murojaat-detail'),
    path('murojaatlar/<int:pk>/status', MurojaatStatusUpdateAPIView.as_view()),
    path('murojaatlar/<int:pk>/status/', MurojaatStatusUpdateAPIView.as_view(), name='murojaat-status-update'),
    path('telegram/webhook/', TelegramWebhookAPIView.as_view(), name='telegram-webhook'),
]
