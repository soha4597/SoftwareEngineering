import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm as BaseUserChangeForm,
    UserCreationForm as BaseUserCreationForm)
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Profile
from .utils import ActivationMailFormMixin

from phonenumber_field.modelfields import PhoneNumberField

logger = logging.getLogger(__name__)

# ActivationMainFormMixin is used ro send the user an email
class ResendActivationEmailForm(
        ActivationMailFormMixin, forms.Form):

    email = forms.EmailField()
    # The form will be invalid if the user doesn't submit a value to email, or submits a value that doesn't represent an email.
    mail_validation_error = (
        'Could not re-send activation email. '
        'Please try again later. (Sorry!)')

    def save(self, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(
                email=self.cleaned_data['email'])
        except: # In case we don't find a user, then  we simply return None and don't raise any exceptions to not entertain malicious attacks
            #logger.warning(
             #   'Resend Activation: No user with '
              #  'email: {} .'.format(
               #     self.cleaned_data['email']))
            return None
        self.send_mail(user=user, **kwargs)
        return user

#Django's BaseUserCreationForm doesn't include the email of the user
class UserCreationForm(
        ActivationMailFormMixin,
        BaseUserCreationForm):

    phone = phone = forms.CharField(
        max_length=9, help_text=("e.g. 70/000001") )
    # phone = PhoneNumberField(null=False, blank=False, unique=True)

    location = forms.CharField(
        max_length=255,
        help_text=(
            "Location to be stored in your "
            "public profile."))

    # We override the mepty string defined in the ActivationMailFormMixin
    mail_validation_error = (
        'User created. Could not send activation '
        'email. Please try again later. (Sorry!)')

    #This MetaClass is inherited from the BaseUserCreationForm
    #It defines the ModelForm Behaviour of our UserCreationForm
    # We define the model and the email, name = username and location fields
    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model() # This is the User Model in the auth app
        fields = ('username', 'email', 'phone', 'location')

    # We make sure that the username doesn't create a conflict in the url path
    # This works on the default user model. To work on the custom usermodel, we change username to name, and define name here and in the profile model
    def clean_username(self):
        name = self.cleaned_data['username']
        # We consider all the prefixes in the users uel
        # that we have or might implement in the future
        # to not create conflict between the potential user
        #profile url at: user/<username>/path
        disallowed = (
            'activate',
            'create',
            'disable',
            'login',
            'logout',
            'password',
            'profile',
        )
        if name in disallowed:
            raise ValidationError(
                "A user with that name"
                " already exists.")
        return name

    # We override the save method of the form, where we will pass the keyword arguments to the send_mail()
    def save(self, **kwargs):
        user = super().save(commit=False) #This creates a user instance from the data in the from without saving it in the database
        if not user.pk:
            user.is_active = False # This disables the account of the user
            send_mail = True
        else:
            send_mail = False #If this user already has a pk, then he is in the databse, so we disable sending the activation mail
        user.save() # After knowing whether or not to send an activation email, we save the user into the database.
        #A side effect of using commit=False is seen when your model has a many-to-many relation with another model.
        # If your model has a many-to-many relation and you specify commit=False when you save a form,
        # Django cannot immediately save the form data for the many-to-many relation.
        # To work around this problem, every time you save a form using commit=False, Django adds a save_m2m() method to your ModelForm subclass.
        # After you’ve manually saved the instance produced by the form, you can invoke save_m2m() to save the many-to-many form data

        self.save_m2m()

        # We want to create a Profile for the user at the moment we are creating this user
        Profile.objects.update_or_create( #This method searches for a profile for the user. If it doesn't find one
            # then it creates a new profile with the user and defaults. Otherwise, it only updates the values in the defaults
            user=user,
            defaults={
                'phone': self.cleaned_data['phone'],
                'location': self.cleaned_data['location'],
                'slug': slugify(
                    user.get_username()), # We generate the slug of he profile using the username
                # and this make the username limited by the values above because the slug is used in the url path
                # In other words, we want the user to access his/her profile at: user/<username>
            })
        if send_mail: # In case we needed to send an email in ActivationMailFormMixin
            self.send_mail(user=user, **kwargs)
        return user # We return the new/updated object based on the convention of the save() method.
