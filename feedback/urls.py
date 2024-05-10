from django.urls import path, include
from . import views
from .views import AboutView, ResourcesView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('resources/', ResourcesView.as_view(), name='resources'),
    path('report/', views.report_view, name='report'),
    path('report/success/', views.report_success_view, name='report_success'),
    path('report-details/<int:report_id>/', views.report_details, name='report_details'),
    path('pending-reports/', views.admin_pending_reports, name='admin_pending_reports'),
    path('submitted-reports/', views.user_submitted_reports, name='user_submitted_reports'),
    path('faq/', views.faq, name='faq'),
]
