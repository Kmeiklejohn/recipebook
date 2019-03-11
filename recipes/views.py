from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponseRedirect, reverse
from recipes.models import Recipe, Author, User
from recipes.forms import Add_Recipe, Add_Author, SignupForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    recipes = Recipe.objects.all()
    recipebook = {'recipes':recipes}
    return render(request, 'index.html', recipebook)

def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipebook = {'recipe': recipe}
    return render(request, 'recipe.html', recipebook)

def author_view(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    recipes = Recipe.objects.filter(author=author)
    recipebook = {'recipes': recipes, 'author': author}
    return render(request, 'author.html', recipebook)

@login_required()
def add_recipe(request):

    form = None
   
    if request.method == 'POST':
        form = Add_Recipe(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title = data['title'],
                description = data['description'],
                instructions = data['instructions'],
                author = data['name'],
                time_required = data['time_required']
                )
            return render(request, 'updated.html')
    else:
        form = Add_Recipe()
        if not request.user.is_staff:  
            form.fields['author'].queryset= Author.objects.filter(user=request.user)
    return render(request,'add_recipe.html', {'form': form} )
    
        

@login_required()
@staff_member_required(login_url='error')
def add_author(request):

    form = None

    if request.method == 'POST':
        form = Add_Author(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data['name'])
            Author.objects.create(
                name = data['name'],
                bio = data['bio'],
                user = new_user
            )
            return render(request, 'updated.html')
    else:
        form = Add_Author()

    return render(request,'add_author.html', {'form': form} )

def signup_view(request):
    
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'], 
                data['email'],
                data['password'])
            login(request, user)
            Author.objects.create(
                name=data['name'],
                user=user
            )
            return HttpResponseRedirect(reverse('index'))    
    else:
        form = SignupForm()
    return render(request, 'generic_form.html', {"form": form})

def login_view(request):
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next','/'))
    else:
        form = LoginForm()
    return render(request, 'generic_form.html', {'form': form})

def logout_view(request):

    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))

def error_view(request):
    return render(request,'error.html')