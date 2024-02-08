from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('attendance/', views.AttendanceView.as_view(), name='attendance'),
    path('attendance/start/', views.StartView.as_view()),
    path('attendance/end/', views.EndView.as_view()),

    path('status/', views.StatusView.as_view(), name='status'),
    path('correction/', views.CorrectionView.as_view(), name='correction'),
    path('allstatus/', views.AllStatusView.as_view(), name='allstatus'),

    path('correction/<str:pk>/<str:id>/', views.UpdateStart),
    path('correction/<str:pk>/<str:id>/', views.UpdateEnd),
]