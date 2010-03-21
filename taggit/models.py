from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models, IntegrityError
from django.template.defaultfilters import slugify


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.generate_slug()
        
        return super(Tag, self).save(*args, **kwargs)
    
    def generate_slug(self):
        """
        Without breaking a transaction, find the next best available slug.
        
        This will try the ``slugify``-ed version first. If that is not
        available, then start appending on an incrementing integer until
        an available slug is found.
        """
        original_slug = slug = slugify(self.name)
        i = 0
        
        while True:
            try:
                found = Tag.objects.get(slug=slug)
                i += 1
                slug = "%s_%s" % (original_slug, i)
            except Tag.DoesNotExist:
                break
        
        return slug


class TaggedItem(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, related_name="tagged_items")
    content_object = GenericForeignKey()
    
    tag = models.ForeignKey(Tag, related_name="items")
    
    def __unicode__(self):
        return "%s tagged with %s" % (self.content_object, self.tag)
