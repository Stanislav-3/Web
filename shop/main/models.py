from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

from django.urls import reverse
from django.utils.text import slugify
from django.contrib import messages
import datetime

# Используем _("Hello") например, и если язык устаановлен в русский то выдаст "Привет" вроде бы.
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=50)

    email_is_verifyed = models.BooleanField(default=False)

    def get_full_name(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    def __str__(self):
        return self.user.username + '_profile'


class Category(models.Model):

    title = models.CharField(max_length=50, verbose_name="title")
    image = models.ImageField(verbose_name="Изображение", default="default_img.jpg") # default Берётся из папки /media/
    slug = models.SlugField(default='', editable=False, max_length=50, unique=True)

    @property
    def get_valid_url_for_products(self):
        return reverse('products_url') + '?' + 'category' + '=' + str(self.slug)

    def save(self, *args, **kwargs):
        from django.template import defaultfilters
        from unidecode import unidecode

        value = self.title
        # Предусматриваем преобразование из Unicode в ASCII.
        self.slug = defaultfilters.slugify(unidecode(value),) # there was also " allow_unicode=True"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

def validate_amount_of_product(value):
    if value > 1000:
        raise ValidationError('Amount could not be bigger than 1000')
    else:
        return value

class Product(models.Model):
    # the name of product field.
    title = models.CharField('Name', max_length=50)
    description = models.TextField('Description', max_length=255, default="Some description ...")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=99.99)
    amount = models.PositiveIntegerField(default=5, validators=[validate_amount_of_product])
    image = models.ImageField(verbose_name="Изображение", default="default_img.jpg") # default Берётся из папки /media/
    slug = models.SlugField(default='', editable=False, max_length=50, unique=True)

    @property
    def get_string_price(self):
        return str(self.price) + '$'

    def get_absolute_url(self):
        return reverse('specific_product_url_with_slug', args=(self.slug,))

    # Переопределяем стандартный метод из Model.Чтобы автоматически записывался slug из title.
    def save(self, *args, **kwargs):
        from django.template import defaultfilters
        from unidecode import unidecode

        self.slug = defaultfilters.slugify(unidecode(self.title),) # there was also " allow_unicode=True"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()