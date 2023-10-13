from django.db import models

# Create your models here.
class information(models.Model):

    commpany_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.IntegerField()
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = "information"
        verbose_name_plural = "informations"

    def __str__(self):
        return self.commpany_name

