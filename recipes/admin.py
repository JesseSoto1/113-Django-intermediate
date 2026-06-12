from django.contrib import admin
from .models import Category, Ingredient, RecipeIngredient, Recipe

# Register your models here.

# admin.site.register([Category, Ingredient, RecipeIngredient, Recipe])


#------------------------Category----------------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display is a tuple that allows us to difine the columns to display in the admin site
    list_display = ('name', 'slug', 'recipe_count')
    # search_fields all0w us to enable the search bar and search thru the desired attributes
    search_fields = ('name', )
    #prepopulated_fields allows us to add values without actually typing a value on it.
    prepopulated_fields = {'slug':('name', )}

    @admin.display(description="# Recipes")
    def recipe_count(self, obj):
        return obj.recipes.count()
    

# --------------------Ingredient--------------------------------

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', ) 
    search_fields = ('name', )


# -------------RecipeIngredients InLine-------------------------------

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3# how many empty rows to show by default
    fields = ('ingredient', 'quantity', 'unit','notes')

# -----------------Recipe--------------------------
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title','author','category','status','prep_time','cook_time', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    prepopulated_fields = {'slug':('title', )}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RecipeIngredientInline]

    fieldsets = (
        ('Main Information', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('Content', {
            'fields': ('description', 'instructions', 'image')
        }),
        ('Times & Servings', {
            'fields':('prep_time', 'cook_time', 'servings')
        }),
        ('Timestamps', {
            'fields': ('created_at','updated_at'),
            'classes': ('collapse', )
        }),
    )