from django import forms

from taggit.forms import TagField
from taggit.tests.models import Food


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food


def space_separated(tags):
    if tags is None:
        tags = ""
    return [o.strip() for o in tags.split() if o.strip()]


class CustomFoodForm(FoodForm):
    tags = TagField(parser=space_separated)
