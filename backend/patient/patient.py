from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
import messages


class Error(Exception):
  pass


class AuthorizedStateError(Error, ValueError):
  pass


class PatientModel(ndb.Model):
  # Key is the patient's primary email address.
  email = ndb.StringProperty()
  message = msgprop.MessageProperty(messages.Patient)


class BaseStorage(object):
  pass


class DbStorage(BaseStorage):

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


class Patient(object):

  def __init__(self, email, storage=DbStorage):
    self.storage = storage(email)

  def to_message(self):
    return self.storage.get_message()

  def get_direct_addresses(self):
    if not self.storage.exists:
      return []
    return self.storage.get_message().direct_addresses

  def add_direct_address(self, email):
    message = self.to_message()
    if not message.direct_addresses:
      message.direct_addresses = []
    if email in message.direct_addresses:
      # TODO: Raise error.
      return
    message.direct_addresses.append(email)
    self.storage.set_message(message)
    self.storage.save()

  def remove_direct_address(self, email):
    message = self.to_message()
    if email not in message.direct_addresses:
      return
    direct_addresses = set(message.direct_addresses)
    direct_addresses.remove(email)
    message.direct_addresses = list(direct_addresses)
    self.storage.set_message(message)
    self.storage.save()

  def set_frequency(self, frequency):
    if frequency == 'NONE':
      frequency = messages.Frequency.NONE
    elif frequency == 'SINGLE':
      frequency = messages.Frequency.SINGLE
    elif frequency == 'CONTINUOUS':
      frequency = messages.Frequency.CONTINUOUS
    else:
      raise Exception
    message = self.to_message()
    message.frequency = frequency
    self.storage.set_message(message)
    self.storage.save()
