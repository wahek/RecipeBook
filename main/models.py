import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    ingredients = models.ManyToManyField('Ingredient')
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(default=None, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    author = models.ForeignKey('User', null=True, related_name='user', on_delete=models.SET_NULL)
    view = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='recipe_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)


class RecipeIngredient(models.Model):
    UNIT_CHOICES = (
        ('g', 'грамм'),
        ('kg', 'килограмм'),
        ('l', 'литр'),
        ('ml', 'миллилитр'),
    )
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=None, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)


class Category(models.Model):
    name = models.CharField(max_length=100)


class RecipeCategory(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class User(AbstractUser):
    gender = models.CharField(max_length=1, choices=[('M', 'Мужчина'), ('F', 'Женщина')])
    birth_date = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True,
                                      validators=[MinValueValidator(1), MaxValueValidator(100)])

    def save(self, *args, **kwargs):
        if self.birth_date:
            days = datetime.date.today() - self.birth_date
            self.age = days.days // 365
        super().save(*args, **kwargs)
