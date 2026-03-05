from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('check-result/', views.check_result, name='check_result'),
    path('schools/', views.get_schools, name='get_schools'),
    path('api/set-school/', views.api_set_school, name='api_set_school'),
    path('api/add-school/', views.api_add_school, name='api_add_school'),
    
    # Dashboard API endpoints
    path('api/results/', views.api_get_results, name='api_get_results'),
    path('api/results/save/', views.api_save_result, name='api_save_result'),
    path('api/results/bulk-save/', views.api_bulk_save_results, name='api_bulk_save_results'),
    path('api/results/delete/<int:result_id>/', views.api_delete_result, name='api_delete_result'),
]