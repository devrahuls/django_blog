from django.db import models

# Create your models here.
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

# A location to save the blog imgs
def upload_location(instance, filename):
    #A defined format to save the blog images
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id = str(instance.author.id),
        title = str(instance.title),
        filename = filename,
    )
    return file_path

class BlogPost(models.Model):
    title                   = models.CharField(max_length=50, null=False, blank=False)
    body                    = models.TextField(max_length=5000, null=False, blank=False)
    image                   = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published          = models.DateTimeField(auto_now_add=True, verbose_name="date_published")
    date_updated            = models.DateField(auto_now=True, verbose_name="date_updated")
    author                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #It looks for an authenticated account and maps a foreign key relationship with the account table to the author.
    #CASCADE - Deletes everything that is related to the author like images, title, body, but not the actual account that it is assciated with it.
    slug                    = models.SlugField(blank=True, unique=True) #Just an URL, that is unique for the every blog post.

    def __str__(self):
        return self.title

#When the Blog Post of a user gets deleted, then also deletes the image from the DB, not just the ref link, but the whole img of the blog post.
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

# Brfore saving the blog post, run this function. It basically, sets a unique url for every blog post by considering the username & the title of the blog.
def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
