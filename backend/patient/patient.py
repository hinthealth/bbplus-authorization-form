from django.core.validators import email_re
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
import os
import messages

SENDER = 'noreply@{}.appspotmail.com'.format(os.environ['APPLICATION_ID'])


class Error(Exception):
  """Module error class."""


class PatientModel(ndb.Model):
  """Datastore model for patient configuration data."""
  # Key is the patient's primary email address.
  email = ndb.StringProperty()
  message = msgprop.MessageProperty(messages.Patient)


class BaseStorage(object):
  """Base storage class."""


class DbStorage(BaseStorage):
  """A storage mechanism that uses App Engine datastore and email API."""

  def __init__(self, email):
    self.email = email
    key = ndb.Key(PatientModel, email)
    entity = key.get()
    self.entity = entity if entity else PatientModel(key=key)

  @property
  def exists(self):
    return bool(self.entity)

  def get_message(self):
    message = self.entity.message
    if not message:
      return messages.Patient()
    return message

  def set_message(self, message):
    self.entity.message = message

  def save(self):
    self.entity.put()

  def send_email_notification(self):
    subject = 'BlueButton+ data push subscription updated'
    body = [
        'Your BlueButton+ data subscription preferences have been updated.\n',
    ]
    addresses = self.get_message().direct_addresses
    if not addresses:
      body.append('No Direct addresses registered.')
    else:
      body.append('You have registered the following Direct addresses:')
      body.extend(addresses)
      body.append('\n')
    frequency = self.get_message().frequency
    body.append('Your data push frequency is:')
    body.append(str(frequency))
    body = '\n'.join(body)
    mail.send_mail(SENDER, self.email, subject, body)


class Patient(object):

  def __init__(self, email, storage=DbStorage):
    self.storage = storage(email)

  def to_message(self):
    """Returns the patient's configuration as a ProtoRPC message."""
    return self.storage.get_message()

  def get_direct_addresses(self):
    """Returns the patient's registered Direct addresses."""
    if not self.storage.exists:
      return []
    return self.storage.get_message().direct_addresses

  def add_direct_address(self, email):
    """Adds a Direct addresss for the patient."""
    message = self.to_message()
    if not message.direct_addresses:
      message.direct_addresses = []

    # Do not allow invalid emails.
    if not email_re.match(email):
      return

    # Do not allow emails that are already registered.
    if email in message.direct_addresses:
      return

    message.direct_addresses.append(email)
    self.storage.set_message(message)
    self.storage.save()

  def remove_direct_address(self, email):
    """Removes a Direct address from the patient's configuration."""
    message = self.to_message()

    # Do not allow removing emails that aren't registered.
    if email not in message.direct_addresses:
      return

    direct_addresses = set(message.direct_addresses)
    direct_addresses.remove(email)
    message.direct_addresses = list(direct_addresses)
    self.storage.set_message(message)
    self.storage.save()

  def set_frequency(self, frequency):
    """Sets the patient's data push frequency."""
    if frequency == 'NONE':
      frequency = messages.Frequency.NONE
    elif frequency == 'SINGLE':
      frequency = messages.Frequency.SINGLE
    elif frequency == 'CONTINUOUS':
      frequency = messages.Frequency.CONTINUOUS
    else:
      raise ValueError('%s is not a valid frequency.' % frequency)
    message = self.to_message()
    message.frequency = frequency
    self.storage.set_message(message)
    self.storage.save()

  def send_email_notification(self):
    self.storage.send_email_notification()
