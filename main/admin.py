from django.contrib import admin
from .models import *
from django.utils.html import format_html
import admin_thumbnails


# Register your models here.

@admin_thumbnails.thumbnail('image')
class imagesTabular(admin.TabularInline):
    model = productGallery
    extra = 1

class categoryAdmin(admin.ModelAdmin):
    def Thumbnail(self,obj):
        return format_html("<img src='{}' width='40px' style='border-radius:50px;'/>".format(obj.cat_image.url))
    Thumbnail.short_description = 'cat_image'
    prepopulated_fields = {'cat_slug':('cat_name',)}
    list_display = ('id','Thumbnail','cat_name')

class productAdmin(admin.ModelAdmin):
    def Thumbnail(self, obj):
        return format_html("<img src='{}' width='40px' style='border-radius:50px;'/>".format(obj.product_image.url) )
    
    Thumbnail.short_description = 'product image'
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('id','Thumbnail','product_name','price','is_available','created','updated')
    list_display_links = ('id','Thumbnail','product_name')
    list_filter = ('price','is_available')
    list_editable = ('is_available',)
    ordering = ('id',)
    inlines = [imagesTabular]

class variationAdmin(admin.ModelAdmin):
    list_display = ('id','product','variation_cat','variation_value','is_active')
    list_editable = ('is_active',)
    ordering = ('-variation_cat',)

admin.site.register(Category, categoryAdmin)
admin.site.register(Product, productAdmin)
admin.site.register(Variation,variationAdmin)
admin.site.register(Review)