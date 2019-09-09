from django.shortcuts import render
from django.http import HttpResponse

"""
dogs = [
  Dog('Michi', 'shiba-inu', 'the cutest', 2),
  Dog('Cookie', 'pug', 'shy newborn ', 0),
  Dog('Mochi', 'corgi', 'stubby happy fluff ball', 3)
]
"""

#create home view
def home(request):
    return render(request, 'home.html')

#create about view
def about(request):
    return render(request, 'about.html')

#create dogs list view
def dogs_index(request):
    return render(request, 'dogs/index.html', {'dogs': dogs})