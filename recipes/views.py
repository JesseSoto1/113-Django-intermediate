from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from .models import Recipe
from .forms import  RecipeForm, RecipeIngredientFormSet
# Create your views here.

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = RecipeIngredientFormSet(
                self.request.POST,
                instance=self.object # Omit on create view
            )
        else:
            context['ingredient_formset'] = RecipeIngredientFormSet(
                instance=self.object
            )
        return context
    
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        ingredient_formset = context['ingredient_formset']

        if ingredient_formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()

            # link formset to the newly created recipe, then save
            ingredient_formset.instance = self.object 
            ingredient_formset.save()

            messages.success(self.request, 'Recipe created successfully!')
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'slug': self.object.slug})
    

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_queryset(self):
        return Recipe.objects.filter(status= 'published').select_related('author', 'category')

class RecipeDetailsView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
        
    def get_queryset(self):
        return Recipe.objects.select_related('author', 'category').prefetch_related('recipe_ingredients__ingredient')

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = RecipeIngredientFormSet(
                self.request.POST,
                instance=self.object # Omit on create view
            )
        else:
            context['ingredient_formset'] = RecipeIngredientFormSet(
                instance=self.object
            )
        return context
    

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        ingredient_formset = context['ingredient_formset']

        if ingredient_formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()

            # link formset to the newly created recipe, then save
            ingredient_formset.instance = self.object 
            ingredient_formset.save()

            messages.success(self.request, 'Recipe updated successfully!')
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'slug': self.object.slug})
    
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/delete.html'
    success_url = reverse_lazy('recipe_list')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Recipe deleted succesfully!')
        return super().form_valid(form)