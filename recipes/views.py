from django.shortcuts import render, get_object_or_404
from recipes.models import Recipe, Author

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