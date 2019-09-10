from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Dog

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

#class for CBV:create
class DogCreate(CreateView):
    model = Dog
    fields = '__all__'
    success_url = '/dogs/'

#class for CBV:update
class DogUpdate(UpdateView):
    model = Dog
    fields = ['breed', 'description']

#class for CBV:delete
class DogDelete(DeleteView):
    model = Dog
    success_url = '/dogs/'

