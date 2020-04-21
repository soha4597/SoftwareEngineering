from django.conf.urls import include, url
from django.contrib.auth import \
    views as auth_views
from django.contrib.auth.forms import \
    AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import (
    RedirectView, TemplateView)

from .views import (
    ActivateAccount, CreateAccount,
    DisableAccount, ProfileDetail, ProfileUpdate,
    PublicProfileDetail, ResendActivationEmail)

#password_urls = [
 #   url(r'^$',
  #      RedirectView.as_view(
   #         pattern_name='dj-auth:pw_reset_start',
    #        permanent=False)),
    #url(r'^change/$',
     #   auth_views.password_change,
      #  {'template_name':
       #     'user/password_change_form.html',
        # 'post_change_redirect': reverse_lazy(
        #    'dj-auth:pw_change_done')},
        #name='pw_change'),
    #url(r'^change/done/$',
     #   auth_views.password_change_done,
      #  {'template_name':
       #     'user/password_change_done.html'},
       # name='pw_change_done'),
    # url(r'^reset/$',
      #  auth_views.password_reset,
       # {'template_name':
        #    'user/password_reset_form.html',
        # 'email_template_name':
         #   'user/password_reset_email.txt',
         # 'subject_template_name':
         #   'user/password_reset_subject.txt',
        # 'post_reset_redirect': reverse_lazy(
         #   'dj-auth:pw_reset_sent')},
        # name='pw_reset_start'),
    # url(r'^reset/sent/$',
      #  auth_views.password_reset_done,
      #  {'template_name':
       #     'user/password_reset_sent.html'},
       # name='pw_reset_sent'),
    # url(r'^reset/'
      #  r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
       # r'(?P<token>[0-9A-Za-z]{1,13}'
       # r'-[0-9A-Za-z]{1,20})/$',
       # auth_views.password_reset_confirm,
       # {'template_name':
        #    'user/password_reset_confirm.html',
        # 'post_reset_redirect': reverse_lazy(
         #   'dj-auth:pw_reset_complete')},
        # name='pw_reset_confirm'),
    # url(r'reset/done/$',
      #  auth_views.password_reset_complete,
      #  {'template_name':
      #      'user/password_reset_complete.html',
      #   'extra_context':
       #      {'form': AuthenticationForm}},
       # name='pw_reset_complete'),
#]

urlpatterns = [
    url(r'^$',
        RedirectView.as_view(
            pattern_name='login',
            permanent=False)),
    # in case the url is user/, we redirect him immediately to the login page.

    url(r'^activate/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        ActivateAccount.as_view(),
        name='activate'),
    # We use the uidb64 and tokn to make sure that the user actually received an activation email
    url(r'^activate/resend/$',
        ResendActivationEmail.as_view(),
        name='resend_activation'), # This is where the activation email is resent.
    url(r'^activate',
        RedirectView.as_view(
            pattern_name=(
                'resend_activation'),
            permanent=False)), # The RedirectView is simply a view that redirects to the given url pattern
    # This catches all the urls that start with activate - it doesn't end with $ - but don't match what is above and redirects them to the Resend Activation View
    # We do this because we don't have a page that matches the prefix activate
    url(r'^create/$',
        CreateAccount.as_view(),
        name='create'), #url to create an account
    # We included in the base from and in the login.html directly under the from.
    url(r'^create/done/$',
        TemplateView.as_view(
            template_name=(
                'user/user_create_done.html')),
        name='create_done'), # TemplateView is used to simply create the template without the need for a view.
   # url(r'^disable/$',
    #    DisableAccount.as_view(),
     #   name='disable'),

    #
    url(r'^login/$',
        auth_views.LoginView.as_view(
        template_name= 'user/login.html'),
        name='login'),  # this is redirect to the view that displays the login page for the user to enter credentials
    url(r'^logout/$',
        auth_views.LogoutView.as_view(
        template_name = 'user/logged_out.html',
        extra_context =
             {'form': AuthenticationForm}),
        name='logout'), #this is redirect to the view that displays logout where the credentials reappear in case the user wants to log in again directly
    #after logging out

    #  url(r'^password/', include(password_urls)),
    url(r'^profile/$',
        ProfileDetail.as_view(),
        name='profile'), # We display the Profile of the user at the static url: user/profile
    url(r'^profile/edit/$',
        ProfileUpdate.as_view(),
        name='profile_update'), # We allow the user to update the profile
    url(r'^(?P<slug>[\w\-]+)/$',
         PublicProfileDetail.as_view(),
         name='public_profile'), # This link would display the profiles of other users
]
