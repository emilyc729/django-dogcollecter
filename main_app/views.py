from django.shortcuts import render
from .models import Dog

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
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', {'dogs': dogs})

#create dogs detail view
def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    return render(request, 'dogs/detail.html', {'dog': dog})