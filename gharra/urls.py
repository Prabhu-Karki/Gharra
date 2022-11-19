from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('allauth.urls')),
    path('', include('mainsite.urls')),
] 
handler404 = "mainsite.views.page_not_found_view"