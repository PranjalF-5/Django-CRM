
from django.urls import path
from . import views ;

urlpatterns = [
    path('', views.first_app_render , name = 'first_render_app'),
    
]
