from django.urls import path
from .views import KorrupsiyaCreateView,KarrupsiyaMalumotListView,KorrupsiyaMalumotDetailView,KorrupsiyaFileListView

urlpatterns = [
    path('korrupsiya/', KorrupsiyaCreateView.as_view(), name='korrupsiya-create'),
    path('karrupsiya-malumot/', KarrupsiyaMalumotListView.as_view(), name='karrupsiya-malumot-list'),
    path('karrupsiya-malumot/<int:pk>/', KorrupsiyaMalumotDetailView.as_view(), name='karrupsiya-malumot-detail'),
    path('korrupsiya-file/', KorrupsiyaFileListView.as_view(), name='korrupsiya-file-list'),
]
