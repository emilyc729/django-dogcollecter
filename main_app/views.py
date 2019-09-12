from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Dog, Toy, Photo
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# protect class based views
from django.contrib.auth.mixins import LoginRequiredMixin
# photos
import uuid
import boto3

# Constants
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'dogcollector-ec'

# create home view


def home(request):
    all_dogs = Dog.objects.all()
    return render(request, 'home.html', {'dogs': all_dogs})

# create about view

def about(request):
    return render(request, 'about.html')

# create dogs list view
@login_required
def dogs_index(request):
    dogs = Dog.objects.filter(user=request.user)
    return render(request, 'dogs/index.html', {'dogs': dogs})

# create dogs detail view
@login_required
def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    toys_dog_doesnt_have = Toy.objects.exclude(
        id__in=dog.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'dogs/detail.html', {
        'dog': dog,
        'feeding_form': feeding_form,
        'toys': toys_dog_doesnt_have
    })

# class for CBV:create


class DogCreate(LoginRequiredMixin, CreateView):
    model = Dog
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/dogs/'

    # associate cat w/ user when valid cat form
    def form_valid(self, form):
        # assign to logged in user
        form.instance.user = self.request.user
        # create model in database
        return super().form_valid(form)

# class for CBV:update


class DogUpdate(LoginRequiredMixin, UpdateView):
    model = Dog
    fields = ['breed', 'description']

# class for CBV:delete 


class DogDelete(LoginRequiredMixin, DeleteView):
    model = Dog
    success_url = '/dogs/'

# add feeding view
@login_required
def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('detail', dog_id=dog_id)


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'
    
    def form_valid(self, form):
        quantity = int(self.request.POST.get('quantity'))
        toy_name = self.request.POST.get('name')
        toy_color = self.request.POST.get('color')
        Toy.objects.bulk_create([Toy(name=toy_name, color=toy_color) for i in range(1, quantity)])
        return super().form_valid(form)


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'


@login_required
def assoc_toy(request, dog_id, toy_id):
    Dog.objects.get(id=dog_id).toys.add(toy_id)
    return redirect('detail', dog_id=dog_id)


@login_required
def diassoc_toy(request, dog_id, toy_id):
    Dog.objects.get(id=dog_id).toys.remove(toy_id)
    return redirect('detail', dog_id=dog_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # create 'user' form object
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # add user to database
            user = form.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            # log user in
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'registration/signup.html', context)


def add_photo(request, dog_id):
    photo_file = request.FILES.get('photo-file', None)
    # make sure a file is uploaded
    if photo_file:
        s3 = boto3.client('s3')
        # random # + file extension(.jpg, .png)
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = Photo(url=url, dog_id=dog_id)
            photo.save()
        except:
            print('An error occurred uploading file to s3')
    return redirect('detail', dog_id=dog_id)
