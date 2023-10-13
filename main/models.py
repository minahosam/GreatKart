from django.db import models
from django.db.models import Avg
from accounts.models import *

# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='cat/',blank=True)
    cat_slug = models.SlugField(max_length=100,unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.cat_name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    product_image = models.ImageField(upload_to='product_image')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    product_category = models.ForeignKey(Category,related_name='p_category',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.product_name
    
    def old_price(self):
        return self.price + 100
    
    def review_average(self):
        average = Review.objects.filter(product=self,status=True).aggregate(avg_value=Avg('rating'))
        avg = 0
        if average['avg_value'] is not None:
            avg = float(average['avg_value'])
        return avg
    
    def countReview(self):
        count = 0
        count = Review.objects.filter(product=self,status=True).count()
        return count

class variationManager(models.Manager):
    def all_colors(self):
        return super(variationManager, self).filter(variation_cat='color',is_active=True)
    
    def all_sizes(self):
        return super(variationManager, self).filter(variation_cat='Size',is_active=True)

    def color_avaliabity(self):
        print(super(variationManager,self).filter(variation_cat='color',is_active=True).count())
        return super(variationManager,self).filter(variation_cat='color',is_active=True).count()
select_variation = (
    ('Size','Size'),
    ('color','color')
)
class Variation(models.Model):
    product = models.ForeignKey(Product, related_name='product_variation',on_delete=models.CASCADE)
    variation_cat = models.CharField(max_length=6,choices=select_variation)
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add= True)
    objects = variationManager()
    def __str__(self):
        return f"{self.variation_cat}       {self.variation_value}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='product_reviews',on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name='user_reviews', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    review = models.TextField()
    rating = models.FloatField()
    ip = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class productGallery(models.Model):
    product = models.ForeignKey(Product,related_name='productImages',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productImages')