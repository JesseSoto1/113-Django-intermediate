from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

# --------------------------Category Model--------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)


    class Meta:# rearrange the displayable items on the admin site
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
# ----------------------------Ingredients Model--------------------------
class Ingredient(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    
    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ['name']
    

    def __str__(self):
        return self.name
    

# ---------------------------ManyToMany------------------------------------
# SIMPLE ManyToMany ---Django automatically creates the junction table
# It only stores both sids ID's. We cant add extra fields
# class Recipe(models.Model):
    # ingredients = models.ManyToManyField(Ingredient)



# ManyToMany with THROUGH we define the junction table ourselves
# we can add whatever fields we need to (qty,units,etc...)
# class Recipe(models.Model):
#     ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")


# -------------------------RecipeIngredient Model (Junction table)------------------------------------
# relation between Reciope---> Ingredient

class RecipeIngredient(models.Model):

    UNIT_CHOICES = [
        ('cup', 'Cup'),
        ('tbsp', 'Tablespoon'),
        ('tsp', 'Teaspoon'),
        ('g', 'Grams'),
        ('kg', 'Kilograms'),
        ('ml', 'Milliliters'),
        ('l', 'Liters'),
        ('oz', 'Ounces'),
        ('lb', 'Pounds'),
        ('piece', 'Piece'),
        ('pinch', 'Pinch'),
        ('to_taste', 'To taste'),
    ]

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='recipe_ingredients')
    
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True)
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        blank=True)
    
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe Ingredients"
        unique_together = ('recipe', 'ingredient')
    

    def __str__(self):
        return f'{self.ingredient.name} -> {self.recipe.title}'

#--------------Image helper function-------------------------------
def recipe_image_path(instance, filename):
    """saves the image to media/recipes/<author_id>/<filename>"""
    return f"recipe/{instance.author.id}/{filename}"

# -------------Recipe Model--------------------
class Recipe(models.Model):

    STATUS_CHOICES = [
        ('draft','Draft'),
        ('published', 'Published'),
    ]

    title= models.CharField(max_length=200)
    slug= models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    instructions = models.TextField()
    prep_time = models.PositiveIntegerField(help_text="Time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Time in minutes")
    servings = models.PositiveIntegerField(default=2)
    image = models.ImageField(
        upload_to=recipe_image_path,
        blank=True,
        null=True
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def total_time(self):
        return self.prep_time + self.cook_time