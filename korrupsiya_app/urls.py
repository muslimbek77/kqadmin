from django.urls import path
from .views import (
    KorrupsiyaCreateView, KarrupsiyaMalumotListView, KorrupsiyaMalumotDetailView,
    KorrupsiyaFileListView, VacancyListAPIView, VacancyDetailAPIView
)

urlpatterns = [
    path('korrupsiya/', KorrupsiyaCreateView.as_view(), name='korrupsiya-create'),
    path('karrupsiya-malumot/', KarrupsiyaMalumotListView.as_view(), name='karrupsiya-malumot-list'),
    path('karrupsiya-malumot/<int:pk>/', KorrupsiyaMalumotDetailView.as_view(), name='karrupsiya-malumot-detail'),
    path('korrupsiya-file/', KorrupsiyaFileListView.as_view(), name='korrupsiya-file-list'),
    path('vacancies/', VacancyListAPIView.as_view(), name='vacancy-list'),
    path('vacancies/<int:pk>/', VacancyDetailAPIView.as_view(), name='vacancy-detail'),
]
