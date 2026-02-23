from django.urls import path
from . import views

urlpatterns = [
    path('', views.ui, name='home'),
    path('search/', views.search_result, name='search_result'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('results/', views.result_list, name='result_list'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('ui', views.home, name='ui'),
    path('results/<str:symbol_number>/', views.result_detail, name='result_detail'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]

handler404 = "results.views.custom_404"
