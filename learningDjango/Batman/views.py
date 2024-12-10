from django.shortcuts import render
from .models import Model1

def first_app_render(request):
    database_model = Model1.objects.all()
    return render(request,'htm_folder/one.html' , {'database_model' : database_model})
   