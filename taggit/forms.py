from django.core.exceptions import ImproperlyConfigured
from django import forms

from taggit.utils import parse_tags


class TagField(forms.CharField):
    def __init__(self, *args, **kwargs):
        if 'parser' in kwargs:
            if not callable(kwargs['parser']):
                raise ImproperlyConfigured("The 'parser' provided must be a callable.")
            
            self.parser = kwargs['parser']
            del(kwargs['parser'])
        else:
            self.parser = parse_tags
        
        super(TagField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        try:
            return self.parser(value)
        except ValueError:
            raise forms.ValidationError("Please provide a comma seperate list of tags.")
