from django.shortcuts import render
from .models import *
from .forms import sign_in, sign_up
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as lg
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q



# Create your views here.
def sign_up_view(request):
    if request.method == 'POST':
        form = sign_up(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if User.objects.filter(username=data['username']).exists():
                context = {
                    'message': 'Username already exists! Choose another one.',
                    'form': form
                }
                return render(request, 'sign_up.html', context)
            else:
                u = User.objects.create_user(username=data['username'], password=data['password'], first_name = data['first_name'], last_name = data['last_name'], email = data['email'])
                context = {
                    'message': 'Sign up complete, Now you have to sign in.',
                    'fail' : False,
                    'form': sign_in()
                }
                return render(request, 'sign_in.html', context)
    else:
        form = sign_up()

    return render(request, 'sign_up.html', {'form': form})


def logout_view(request):
    logout(request)

    return index(request)

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = sign_in(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # A backend authenticated the credentials
                lg(request, user)
                latest = Movie.objects.all().order_by('id').reverse()[0:8]
                if request.user.is_authenticated:
                    tickets = Ticket.objects.filter(user = request.user)
                else:
                    tickets = []
                context = {"movies": latest,"is_authenticated": request.user.is_authenticated, 'tickets': tickets}
                return render(request, 'index.html', context)
            else:
                # No backend authenticated the credentials
            # redirect to a new URL:
                context = {
                    'form': form,
                    "message": "wrong username or password",
                    'fail': True
                    }
                return render(request, 'sign_in.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = sign_in()

    return render(request, 'sign_in.html', {'form': form})


def index(request):
    latest = Movie.objects.all().order_by('id').reverse()[0:8]
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user = request.user)     
    else:
        tickets = []

    context = {
        'tickets': tickets,
        "movies": latest,
        "is_authenticated": request.user.is_authenticated
    }
    return render(request, 'index.html', context)

def movie_render(request, movie_id):
    movie = Movie.objects.filter(id = movie_id).get()
    flag = False
    if int(movie.age_restriction) == 0:
        flag = True
    if request.user.is_authenticated:         
        tickets = Ticket.objects.filter(user = request.user)     
    else:         
        tickets = []

    context = {
        'tickets': tickets,
        "movie": movie,
        "flag": flag,
        "is_authenticated": request.user.is_authenticated
         }
    return render(request, 'movie.html', context)

@login_required(login_url = '/sign_in')
def reserve(request, movie_id):
    movie = Movie.objects.filter(id = movie_id).get()

    st = Showtimes.objects.filter(movie = movie_id).filter(active = True).exclude(remaining_cap = 0)
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user = request.user)     
    else:         
        tickets = []

    context = {
        'tickets': tickets,
        'movie': movie,
        'showtimes': st,
        'user': request.user,
        'is_authenticated': request.user.is_authenticated

    }
    print(st)
    return render(request, 'reservation.html', context)

@csrf_exempt
@login_required(login_url = '/sign_in')
def check(request):
    number = request.POST['num']
    option = request.POST['option']
    selected = Showtimes.objects.get(id = option)
    movie = selected.movie
    if request.user.is_authenticated:         
        tickets = Ticket.objects.filter(user = request.user)     
    else:         
        tickets = []

    if selected.remaining_cap < int(number):
        context = {
            'tickets': tickets,
            'movie': movie, 
            'message': 'Sorry! Not enough seats',
            'is_authenticated': request.user.is_authenticated
        }
        return render(request, 'reservation.html', context)

    else:
        tic = Ticket(user = request.user, showtime = selected, seats = number)
        tic.save()
        latest = Movie.objects.all().order_by('id').reverse()[0:8]
        selected.remaining_cap -= int(number)
        selected.save()
        if request.user.is_authenticated:         
            tickets = Ticket.objects.filter(user = request.user)     
        else:         
            tickets = []

        context = {
            'tickets' : tickets,
            'message' : True,
            "movies": latest,
            "is_authenticated": request.user.is_authenticated
        }

        return render(request, 'index.html', context)
        

@csrf_exempt
def search(request):
    keyword = request.POST['keyword']
    lookups= Q(title__icontains=keyword) | Q(cast__icontains=keyword) | Q(director__icontains=keyword) | Q(categories__name__icontains=keyword)

    res = Movie.objects.filter(lookups).distinct()
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user = request.user)     
    else:         
        tickets = []

    context = {
        'tickets': tickets,
        'keyword': keyword,
        'result': res,
        'is_authenticated': request.user.is_authenticated

    }
    return render(request, 'search.html', context)


def movies_render(request):
    movies = Movie.objects.all()
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user = request.user)
    else:
        tickets = []
    context = {
        'tickets': tickets,
        'is_authenticated': request.user.is_authenticated,
        'result': movies
    }

    return render(request, 'movies.html', context)


def cinemas_render(request):
    cinemas = Cinema.objects.all()
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user = request.user)
    else:
        tickets = []
    context = {
        'tickets': tickets,
        'is_authenticated': request.user.is_authenticated,
        'result': cinemas
    }

    return render(request, 'cinemas.html', context)