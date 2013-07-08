from protorpc import messages

class Frequency(messages.Enum):
  NONE = 0
  SINGLE = 1
  CONTINUOUS = 2

class Patient(messages.Message):
  patient_email = messages.StringField(1)
  direct_addresses = messages.StringField(2, repeated=True)
  frequency = messages.EnumField(Frequency, 3)
