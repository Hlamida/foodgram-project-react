# Generated by Django 3.2.16 on 2023-02-11 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='cart',
            name='unique_recipe_cart',
        ),
        migrations.RemoveConstraint(
            model_name='recipeingredients',
            name='unique_recipe',
        ),
    ]