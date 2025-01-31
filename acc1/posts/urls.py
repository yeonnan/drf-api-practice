from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailAPIView.as_view(), name='post-detail'),
]
