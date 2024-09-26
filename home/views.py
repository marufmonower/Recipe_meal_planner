from django.shortcuts import render, redirect
from .models import Recipe
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout


@login_required(login_url='/login/')
def recipes(request):
    # Handle POST request to create a new recipe
    if request.method == 'POST':
        data = request.POST
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')

        # Create a new recipe entry
        Recipe.objects.create(
            day=day,
            name=name,
            description=description,
        )

        # Redirect back to the recipe page after successful creation
        return redirect('/recipes/')

    # Handle GET request to display recipes
    queryset = Recipe.objects.all()

    # If there is a search query, filter the queryset
    if request.GET.get('search'):
        queryset = queryset.filter(
            day__icontains=request.GET.get('search')
        )

    # Prepare the context
    context = {'recipes': queryset}

    # Render the template with the context
    return render(request, 'recipe.html', context)


@login_required(login_url='/login/')
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')

        queryset.day = day
        queryset.name = name
        queryset.description = description
        queryset.save()
        return redirect('/recipes/')

    # Prepare the context
    context = {'recipe': queryset}

    # Render the update recipe template
    return render(request, 'update_recipe.html', context)


@login_required(login_url='/login/')
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes/')


def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = authenticate(username=username, password=password)

            if user_obj is not None:
                login(request, user_obj)
                return redirect('/recipes/')

            messages.error(request, "Invalid username or password")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/login/')

    return render(request, "login.html")


def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    return render(request, "register.html")

# logout function


def custom_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def pdf(request):
    if request.method == 'POST':
        data = request.POST
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')

        Recipe.objects.create(
            day=day,
            name=name,
            description=description,
        )

        return redirect('pdf')
    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(
            day__icontains=request.GET.get('search')
        )
    context = {'recipes': queryset}
    return render(request, 'pdf.html', context)
