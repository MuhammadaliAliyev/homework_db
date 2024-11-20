from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from bot.utils.functions import send_user_created_message as notify
from asgiref.sync import async_to_sync
from bot.utils.db_api.db import get_tg_user_by_phone


# custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, first_name='user', **extra_fields):
        if not first_name:
            raise ValueError("The first_name field must be set.")
        user = self.model(phone_number=phone_number, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, first_name='admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, first_name=first_name, **extra_fields)
    
    def save(self, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class PhoneNumbers(models.Model):
    kitchen = models.ForeignKey('Kitchen', on_delete=models.CASCADE, related_name='phone_numbers')
    title = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.title


class SocialLinks(models.Model):
    kitchen = models.ForeignKey('Kitchen', on_delete=models.CASCADE, related_name='social_links')
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.title

# Kitchens
class Kitchen(models.Model):
    kitchen_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='kitchen/images/', null=True, blank=True)
    background = models.ImageField(upload_to='kitchen/backgrounds/', null=True, blank=True)
    title = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, default="", null=True, blank=True)
    service_fee_text = models.CharField(max_length=255, null=True, blank=True)
    service_fee_amount = models.PositiveIntegerField(default=0)
    rate = models.FloatField(default=0.0)
    slug = models.SlugField(unique=True, unique_for_date='created', max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    get_orders = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    telegram = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = 'Oshxonalar'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Kitchen.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# Custom User
class User(AbstractBaseUser, PermissionsMixin):

    type_choices = [('user', 'User'), ('manager', 'Manager'), ('employee', 'Employee')]

    phone_number = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_kitchen = models.BooleanField(default=False)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.SET_NULL, null=True, blank=True)
    user_type = models.CharField(max_length=255, choices=type_choices, default='user')

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.phone_number



class EmployeeProfile(models.Model):
    kitchen = models.ForeignKey('Kitchen', on_delete=models.CASCADE, related_name='employees')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employees')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


    def __str__(self) -> str:
        return self.full_name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    username = models.CharField(max_length=255, unique=True)
    picture = models.ImageField(upload_to='users/pictures/', default="default-user-image.jpg", null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    tg_profile = models.ForeignKey('botapp.BotUsers', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    @property
    def full_name(self):
        return str(self.first_name) + ' ' + str(self.last_name)


    def __str__(self) -> str:
        return self.first_name
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_kitchen:
            # Create EmployeeProfile for kitchen user
            EmployeeProfile.objects.create(
                user=instance, 
                first_name=str(instance.full_name.split()[0]),
                kitchen_id=instance.kitchen.id
                )
        else:
            # Create UserProfile for regular user
            tg_profile = async_to_sync(get_tg_user_by_phone)(instance.phone_number)
            if tg_profile:
                UserProfile.objects.create(
                    user=instance, 
                    username=instance.phone_number,
                    first_name=tg_profile.first_name,
                    tg_profile=tg_profile
                    )
            else:
                UserProfile.objects.create(user=instance, username=instance.phone_number, first_name=instance.full_name)
            
            # notify user about successful registration via telegram
            async_to_sync(notify)(instance.phone_number)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_kitchen:
        # Save EmployeeProfile for kitchen user
        # instance.employeeprofile.save()
        pass
    else:
        # Save UserProfile for regular user
        instance.profile.save()


class KitchenOrderReceiver(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='order_receivers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_receivers')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user.full_name) + ' - ' + str(self.kitchen.title)
    
