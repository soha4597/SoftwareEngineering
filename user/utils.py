import logging
import traceback
from logging import CRITICAL, ERROR
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.sites.shortcuts import \
    get_current_site
#The core app contains migrations for creating a site
from django.core.exceptions import ValidationError
from django.core.mail import (
    BadHeaderError, send_mail)
from django.template.loader import \
    render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import \
    urlsafe_base64_encode

logger = logging.getLogger(__name__)


class ActivationMailFormMixin:
    mail_validation_error = ''

# The logger; It reports problems.
    def log_mail_error(self, **kwargs):
        msg_list = [
            'Activation email did not send.\n',
            'from_email: {from_email}\n'
            'subject: {subject}\n'
            'message: {message}\n',
        ]
        recipient_list = kwargs.get(
            'recipient_list', [])
        for recipient in recipient_list:
            msg_list.insert(
                1, 'recipient: {r}\n'.format(
                    r=recipient))
        if 'error' in kwargs:
            level = ERROR
            error_msg = (
                'error: {0.__class__.__name__}\n'
                'args: {0.args}\n')
            error_info = error_msg.format(
                kwargs['error'])
            msg_list.insert(1, error_info)
        else:
            level = CRITICAL
        msg = ''.join(msg_list).format(**kwargs)
        logger.log(level, msg)

    #  @property (this is a getter) is used to give "special" functionality to certain methods to make them
    #  act as getters, setters, or deleters when we define properties in a class.
    @property
    def mail_sent(self):
        if hasattr(self, '_mail_sent'):
            return self._mail_sent
        return False

    #This is the setter property, we disable developpers from oerwriting it
    @mail_sent.setter
    def set_mail_sent(self, value):
        raise TypeError(
            'Cannot set mail_sent attribute.')

    # render_to_string() loads a template, and calls its render() method immediately.
    #It leads to raw rendiering of a template to a string.
    def get_message(self, **kwargs):
        email_template_name = kwargs.get(
            'email_template_name')
        context = kwargs.get('context')
        return render_to_string(
            email_template_name, context)

    def get_subject(self, **kwargs):
        subject_template_name = kwargs.get(
            'subject_template_name')
        context = kwargs.get('context')
        subject = render_to_string(
            subject_template_name, context)
        # subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        return subject

    def get_context_data(
            self, request, user, context=None):
        if context is None:
            context = dict()
        current_site = get_current_site(request) #We have only one site, cz we have only one website, but this makes the code more robust
        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'
        token = token_generator.make_token(user) #used for cryptography to prove to the view that the user is allowed to make this request
        uid = urlsafe_base64_encode(
            force_bytes(user.pk)) #user id in base 64, that's how it must be.
        context.update({
            'domain': current_site.domain,
            'protocol': protocol,
            'site_name': current_site.name,
            'token': token,
            'uid': uid,
            'user': user,
        })
        return context

    def _send_mail(self, request, user, **kwargs):
        kwargs['context'] = self.get_context_data(
            request, user)
        mail_kwargs = {
            "subject": self.get_subject(**kwargs),
            "message": self.get_message(**kwargs),
            "from_email": (
                settings.DEFAULT_FROM_EMAIL),
            "recipient_list": [user.email],
        }
        try:
            # number_sent will be 0 or 1
            number_sent = send_mail(**mail_kwargs) # This actually sends the email, imported from the core
        except Exception as error: # We catch the different errors
            self.log_mail_error(
                error=error, **mail_kwargs)
            if isinstance(error, BadHeaderError):
                err_code = 'badheader'
            elif isinstance(error, SMTPException):
                err_code = 'smtperror'
            else:
                err_code = 'unexpectederror'
            return (False, err_code) # We return to the from _send_mail a tuple of boolean false and the error code
        else: # This is in the case where no exception is raised
            if number_sent > 0: #We make sure that the email was sent
                return (True, None) #We return a tuple because we previously returned a typle; better to be consistent with what we reuturn; None means no error
        self.log_mail_error(**mail_kwargs)  #This is executed in the case where mail_sent = 0 and no exception arised.
        return (False, 'unknownerror') #In this case, we return an unknownerror, but it's very unlikely to occur

    # This is what the developper actually calls to send the email.
    def send_mail(self, user, **kwargs):
        request = kwargs.pop('request', None)
      #We can use a logger to report to the developper that the request must be included
        if request is None:
            tb = traceback.format_stack()
            tb = ['  ' + line for line in tb]
            logger.warning(
                'send_mail called without '
                'request.\nTraceback:\n{}'.format(
                    ''.join(tb)))
            self._mail_sent = False
        # return self.mail_sent
        self._mail_sent, error = (
            self._send_mail(
                request, user, **kwargs))
        if not self.mail_sent:
            self.add_error( # We add the error to our form
                None,  # no field - form error
                ValidationError(
                    self.mail_validation_error, # tHIS IS THE ERROR attribute declared at the beginning
                    code=error))
        return self.mail_sent #In all cases, we return the mail_sent attribute

# This is what the views will inherit. It makes sure that the request is included in the keyword arguments
class MailContextViewMixin:
    email_template_name = 'user/email_create.txt'
    subject_template_name = (
        'user/subject_create.txt')

    # We create a dictionary with the keyword arguments for send_mail()
    def get_save_kwargs(self, request):
        return {
            'email_template_name':
                self.email_template_name,
            'request': request,
            'subject_template_name':
                self.subject_template_name,
        }

# This class is inherited by every view that needs to access the Profile
class ProfileGetObjectMixin:

    def get_object(self, queryset=None):
        current_user = get_user(self.request)
        return current_user.profile
