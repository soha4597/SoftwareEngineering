from datetime import date

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,
    PermissionsMixin)
from django.urls import reverse
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


# This model is used to add additional information about the customer (user)
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #This points to the user model in the auth app

    phone = models.CharField(
        max_length=9, help_text=("e.g. 70/000001") )
    # phone = PhoneNumberField(null=False, blank=False, unique=True)
    location = models.CharField(
        max_length=255)
    slug = models.SlugField(
        max_length=30,
        unique=True) # The slug field is used to display the Profile model
    # This is the most up-to-date time for when the profile was updated
    joined = models.DateTimeField(
        "Date Joined",
        auto_now_add=True)

    def __str__(self):
        return self.user.get_username()

    # This allows us to quickly get the url pattern sing the profile object
    # to call public profile. May be needed in the future.
    def get_absolute_url(self):
        return reverse(
            'public_profile',
            kwargs={'slug': self.slug})

    # This allows us to quickly get the url pattern sing the profile object
    # to call profile update
    def get_update_url(self):
        return reverse('profile_update')


# Manager class written to make the interaction with the User Model easier
#class UserManager(BaseUserManager):
 #   use_in_migrations = True #This allows us the manager to interact with the User Model in the migrations

    # This is helper function that will be used to create both users and superusers.
  #  def _create_user(
   #         self, email, password, **kwargs):
    #    email = self.normalize_email(email) # This method from BaseUserManager normalizes the domain (lowercase the domain...) of the email
     #   is_staff = kwargs.pop('is_staff', False)
      #  is_superuser = kwargs.pop(
       #     'is_superuser', False)
        # After assigning the above from the keyword arguments, we create a user instance from our custom model and save it to the database.
       # user = self.model(
        #    email=email,
         #   is_active=True,
          #  is_staff=is_staff,
           # is_superuser=is_superuser,
         #   **kwargs)
        # user.set_password(password)
      #  user.save(using=self._db)
      #  return user

   # def create_user(
    #        self, email, password=None,
     #       **extra_fields):
    #    return self._create_user(
    #        email, password, **extra_fields)

  #  def create_superuser(
   #         self, email, password,
    #        **extra_fields):
     #   return self._create_user(
      #      email, password,
       #     is_staff=True, is_superuser=True,
        #    **extra_fields)

    # def get_by_natural_key(self, email):
      #  return self.get(email=email)

# Not used; In case we want to create a Custom user model
#Having this allows us to remove/modify fields in the default User Model by moving these fields to the
# Profile Model instead. Thus, the custom user model is defined to contain minimal information
# and the rest is put in the Profile Model along with the other fields: name, location...
# This can be used in the future in case we want to allow the user to modify information such as username
# To use it we put in settings the following: AUTH_USER_MODEL = 'user.User'
#class User(AbstractBaseUser, PermissionsMixin):
 #   email = models.EmailField(
  #      'email address',
   #     max_length=254,
    #    unique=True)
    # is_staff should be true for the user to use the admin app
   # is_staff = models.BooleanField(
    #    'staff status',
     #   default=False,
      #  help_text=(
       #     'Designates whether the user can '
        #    'log into this admin site.'))
    #is_active should be true for the user to be able to log in
   # is_active = models.BooleanField(
    #    'active',
     #   default=True,
      #  help_text=(
       #     'Designates whether this user should '
        #    'be treated as active. Unselect this '
         #   'instead of deleting accounts.'))

   # USERNAME_FIELD = 'email' #This is in contrast to the default user model where the username us the name.

   # objects = UserManager() # This makes the manager of out class, the UserManager Class

   # def __str__(self):
   #     return self.email

   # def get_absolute_url(self):
    #    return self.profile.get_absolute_url()

   # def get_full_name(self):
   #     return self.profile.name

   # def get_short_name(self):
    #    return self.profile.name

    # def natural_key(self):
      #  return (self.email,)
