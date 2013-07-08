"""Request handlers for the WSGI application."""

from backend import patient
from google.appengine.api import users
import jinja2
import os
import webapp2


_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
_LOADER = jinja2.FileSystemLoader(_TEMPLATES_DIR)
_ENVIRONMENT = jinja2.Environment(
    loader=_LOADER,
    autoescape=True,
    trim_blocks=True,
)


class BaseHandler(webapp2.RequestHandler):
  """Base request handler class."""

  def __init__(self, *args, **kwargs):
    super(BaseHandler, self).__init__(*args, **kwargs)
    self.user = users.get_current_user()

  def render_to_response(self, template_name, context=None):
    context = {} if context is None else context
    context.update({
        'Frequency': patient.messages.Frequency,
        'login_url': users.create_login_url(self.request.path),
        'logout_url': users.create_logout_url(self.request.path),
        'request': self.request,
        'user': self.user,
    })
    if self.user:
      context['patient'] = patient.Patient(self.user.email())
    template = _ENVIRONMENT.get_template(template_name)
    self.response.write(template.render(**context))


class MainHandler(BaseHandler):
  """Main handler for requests to the App Engine application."""

  def get(self):
    context = {}
    self.render_to_response('main.html', context=context)

  def post(self):
    self.render_to_response('main.html')


class AddDirectAddressHandler(BaseHandler):

  def post(self):
    if not self.user:
      self.abort(400)
    patient_obj = patient.Patient(self.user.email())
    patient_obj.add_direct_address(self.request.POST['direct_address'])
    self.redirect('/?saved')


class RemoveDirectAddressHandler(BaseHandler):

  def post(self):
    if not self.user:
      self.abort(400)
    patient_obj = patient.Patient(self.user.email())
    patient_obj.remove_direct_address(self.request.POST['direct_address'])
    self.redirect('/?saved')


class UpdateFrequencyHandler(BaseHandler):

  def post(self):
    if not self.user:
      self.abort(400)
    patient_obj = patient.Patient(self.user.email())
    patient_obj.set_frequency(self.request.POST['frequency'])
    patient_obj.send_email_notification()
    self.redirect('/?saved')
