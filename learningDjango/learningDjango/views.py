from django.http import HttpResponse
from django.shortcuts import render
 



def home(request):
   #return HttpResponse("I am in Home Route")
   return render(request, 'website/index.html')

