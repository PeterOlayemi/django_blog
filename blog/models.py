from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager

from account.models import User

# Create your models here.

class Category(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=99, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='article_category')
    tag = TaggableManager()
    title = models.CharField(max_length=99, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images')
    likes = models.ManyToManyField(User, related_name='article_like', blank=True)
    views = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title + ' by ' + self.writer.username
    
    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])
    
    def number_of_likes(self):
        return self.likes.count()

class Comment(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.content)[:50] or "comment"  
            slug = base_slug
            counter = 1

            while Comment.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.writer} comments - {self.content[:20]}"

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
