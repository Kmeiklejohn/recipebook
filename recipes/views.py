from django.shortcuts import render, get_object_or_404
from recipes.models import Recipe, Author, User
from recipes.forms import Add_Recipe, Add_Author

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
                author = data['author'],
                time_required = data['time_required']
            )
            return render(request, 'updated.html')
    else:
        form = Add_Recipe()

    return render(request,'add_recipe.html', {'form': form} )

def add_author(request):

    form = None

    if request.method == 'POST':
        form = Add_Author(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name = data['name'],
                bio = data['bio'],
                user = data['user']
            )
            return render(request, 'updated.html')
    else:
        form = Add_Author()

    return render(request,'add_author.html', {'form': form} )