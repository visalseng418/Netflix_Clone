from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Movie
from .models import MovieList
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import re

# Create your views here.
@login_required
def index(request):
    movies = Movie.objects.all()
    action_movies = Movie.objects.filter(genre = "action")
    drama_movies = Movie.objects.filter(genre = "drama")
    featured_movie = movies[len(movies)-1]
    
    context = {
         'movies': movies,
         'action_movies': action_movies,
         'drama_movies' : drama_movies,
         'featured_movie': featured_movie

    }

    return render(request, "index.html", context)

@login_required
def movie(request, pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id = movie_uuid)

    context = {
         'movie_details': movie_details
    }

    return render(request, 'movie.html', context)

@login_required
def search(request):
    if request.method == "POST":
        search_term = request.POST['search_term']
        movies = Movie.objects.filter(title__icontains = search_term)

        context = {
            'movies': movies,
            'search_term': search_term,
        }

        return render(request, 'search.html', context)
    else:
        return redirect('/')

@login_required
def genre(request, pk):
    movie_genre = pk
    movies = Movie.objects.filter(genre = movie_genre)

    context = {
        'movies': movies,
        'movie_genre': movie_genre
    }

    return render(request, 'genre.html' ,context)


@login_required
def my_list(request):
    movie_list = MovieList.objects.filter(owner = request.user)
    user_movie_list = []

    for movie in movie_list:
        user_movie_list.append(movie.movie)

    context = {
        'movies': user_movie_list

    }
    
    return render(request, 'my_list.html', context)

@login_required
def add_to_list(request):
    if request.method == "POST":
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern =  r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id )
        movie_id = match.group() if match else None

        movie = get_object_or_404(Movie, uu_id = movie_id)
        movie_list, created = MovieList.objects.get_or_create(owner = request.user, movie = movie)

        if created:
            response_data = {'status': 'success', 'message': 'Added'}
        else :
            response_data = {'status': 'info', 'message': 'Movie already added.'}
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status = 400)
    
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        pwd  = request.POST['password']

        user = authenticate(request, username = username, password = pwd)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.info(request, "Failed to log in")
            return redirect("login")
        
    return render(request, 'login.html')


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')  # Change 'home' to the name of the page you want to redirect to
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

@unauthenticated_user
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        pwd = request.POST['password']
        confirm_pwd = request.POST['password2']

        if pwd == confirm_pwd:
            try:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email already exists.")
                    return redirect("signup")
                elif User.objects.filter(username=username).exists():
                    messages.info(request, "Username already exists.")
                    return redirect("signup")
                else:
                        user  = User.objects.create_user(username=username, email=email, password=pwd)
                        user.save()
                        login(request, user)
                        return redirect("/")
            except Exception as e:
                        messages.info(request,"Failed to create account")
                        return redirect("signup")
               
        else:
            messages.info(request, "Password do not match.")
            return redirect("signup")

    return render(request, 'signup.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")
