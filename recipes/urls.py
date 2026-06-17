from django.urls import path
from.views import(
    RecipeCreateView,
    RecipeListView,
    RecipeDetailsView,
    RecipeDeleteView,
    RecipeUpdateView

)

urlpatterns = [
    path('create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('<slug:slug>/', RecipeDetailsView.as_view(), name='recipe_detail'),
    path('<slug:slug>/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('<slug:slug>/', RecipeDeleteView.as_view(), name='recipe_delete'),
]