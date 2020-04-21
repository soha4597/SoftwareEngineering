from django.conf import settings
from django.contrib.auth import (
    get_user, get_user_model, logout)
from django.contrib.auth.decorators import \
    login_required
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.messages import error, success
#Meesafes app uses middleware class to temporarily store data in one request and display it in the template
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.template.response import \
    TemplateResponse
from django.utils.decorators import \
    method_decorator
from django.utils.encoding import force_text
from django.utils.http import \
    urlsafe_base64_decode
from django.views.decorators.cache import \
    never_cache
from django.views.decorators.csrf import \
    csrf_protect
from django.views.decorators.debug import \
    sensitive_post_parameters
from django.views.generic import DetailView, View

from core.utils import UpdateView

from .decorators import class_login_required
from .forms import (
    ResendActivationEmailForm, UserCreationForm)
from .models import Profile
from .utils import (
    MailContextViewMixin, ProfileGetObjectMixin)


class ActivateAccount(View):
    success_url = reverse_lazy('login')
    template_name = 'user/user_activate.html'

    # We use this decorator so that we never display outdated information for the user due to caching.
    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            # urlsafe_base64_decode()
            #     -> bytestring in Py3
            uid = force_text(
                urlsafe_base64_decode(uidb64)) # This converts the base 64 to base 10. The function returns bytes so we force it into strings
            user = User.objects.get(pk=uid) # We get the user instance that we want to activate
        except (TypeError, ValueError,
                OverflowError, User.DoesNotExist):
            user = None # If anything goes wrong, we set the user variable to None

        if (user is not None
                and token_generator
                .check_token(user, token)):
            user.is_active = True #We activate the account of the user
            user.save() # We save this change
            success(
                request,
                'User Activated! '
                'You may now login.')
            # We use the messages app to inform the user that the account has been activated
            return redirect(self.success_url) # We redirect to the login page
        else: # If the user is not found or the token in the url path is not valid, then we display the activate.html
            return TemplateResponse(
                request,
                self.template_name)


class CreateAccount(MailContextViewMixin, View):
    #These are the attributes needed in the CreateAccount CBV
    form_class = UserCreationForm
    success_url = reverse_lazy(
        'create_done')
    template_name = 'user/user_create.html'

    # We use this decorator just in case the midddleware or context processor got
    # disables, we we are making sure that the view has a csrf token.
    @method_decorator(csrf_protect)
    def get(self, request):
        # This is equivalent to HttpResponse that renders the template to the user.
        # The template in this case gets rendered in the middleware
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()})

    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters(
        'password1', 'password2'))
    # The last decorator makes django not process these fields in errors nor cache them
    # in order not to accidentally display them to other users/developers.
    def post(self, request):
        bound_form = self.form_class(request.POST)
        # request.POST is a dictionary that has the data, which allows us to directly bind it to the from.
        if bound_form.is_valid():
            # not catching returned user
            # We save the input of user data in the database
            # This also sends the activation email because we overwrote the save method in the UserCreationForm
            # We use the ** to pass the dictionary as a keyword argument
            bound_form.save(
                **self.get_save_kwargs(request))

            if bound_form.mail_sent:  # mail sent?
                return redirect(self.success_url)
            else:
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err) # We pull the errors out of the from and use the error() method
                    # of the messages app to store them. This makes sure that the user sees the error and understands what happened.
                return redirect(
                    'resend_activation')
        # This redisplays the form with the errors since it wasn't valid
        return TemplateResponse(
            request,
            self.template_name,
            {'form': bound_form})

# NOT USED, maybe in the future
class DisableAccount(View):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = (
        'user/user_confirm_delete.html')

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name)

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request):
        user = get_user(request)
        user.set_unusable_password()
        user.is_active = False
        user.save()
        logout(request)
        return redirect(self.success_url)


@class_login_required
class ProfileDetail(
        ProfileGetObjectMixin, DetailView):
    model = Profile
# The Detail View class simply uses the model to display details about it and renders these
# detail in a template name: <model>_detail that we write ourselves.

# Not used, maybe in the future
class PublicProfileDetail(DetailView):
    model = Profile

# Similirly, the UpdateView display a form: <model>_form_update for the user to update hi information in the Profile model
@class_login_required
class ProfileUpdate(
        ProfileGetObjectMixin, UpdateView):
    fields = ('phone','location',) # These are the fields that the user can update in the profile
    model = Profile


class ResendActivationEmail(
        MailContextViewMixin, View):
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('login')
    template_name = 'user/resend_activation.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()})

    @method_decorator(csrf_protect)
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(
                **self.get_save_kwargs(request))
            if (user is not None
                    and not bound_form.mail_sent): # In case the user exists, but we couldn't send the email, we must let the user know through the messages app
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                if errs: # We want to remove the errors in the error list
                    bound_form.errors.pop(
                        '__all__')
                # We redisplay the resend activation form
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'form': bound_form})
        success(
            request,
            'Activation Email Sent!')
        return redirect(self.success_url) # In all cases we redirect to the login page even if the resent was not successful
