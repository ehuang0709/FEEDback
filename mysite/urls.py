from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView



urlpatterns = [
    #path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('', RedirectView.as_view(url='home/', permanent=False)),
    path('home/', include('feedback.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

]