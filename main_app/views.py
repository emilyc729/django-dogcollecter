from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Dog, Toy
from .forms import FeedingForm

# create home view
def home(request):
    return render(request, 'home.html')

# create about view
def about(request):
    return render(request, 'about.html')

# create dogs list view
def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', {'dogs': dogs})

# create dogs detail view
def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    toys_dog_doesnt_have = Toy.objects.exclude(id__in = dog.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'dogs/detail.html', {
        'dog': dog,
        'feeding_form': feeding_form,
        'toys': toys_dog_doesnt_have
    })

# class for CBV:create
class DogCreate(CreateView):
    model = Dog
    fields = '__all__'
    success_url = '/dogs/'

# class for CBV:update
class DogUpdate(UpdateView):
    model = Dog
    fields = ['breed', 'description']

# class for CBV:delete
class DogDelete(DeleteView):
    model = Dog
    success_url = '/dogs/'

# add feeding view
def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('detail', dog_id=dog_id)

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

def assoc_toy(request, dog_id, toy_id):
    Dog.objects.get(id=dog_id).toys.add(toy_id)
    return redirect('detail', dog_id=dog_id)

def diassoc_toy(request, dog_id, toy_id):
    Dog.objects.get(id=dog_id).toys.remove(toy_id)
    return redirect('detail', dog_id=dog_id)