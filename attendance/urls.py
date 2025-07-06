from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clock-in/', views.clock_in, name='clock_in'),
    path('clock-out/', views.clock_out, name='clock_out'),
    path('break-start/', views.break_start, name='break_start'),
    path('break-end/', views.break_end, name='break_end'),
    path('login/', LoginView.as_view(template_name='attendance/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('history/', views.history, name='history'),
    path('edit/<int:pk>/', views.edit_attendance, name='edit_attendance'),
]