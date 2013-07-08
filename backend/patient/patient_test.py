"""Unit tests for patient.py."""

import patient
import unittest2


class PatientTestCase(unittest2.TestCase):

  def testAuthorization(self):
    patient_obj = patient.Patient('user@example.com')
    self.assertFalse(patient.has_authorized())
    patient_obj.authorize(frequency=patient.Frequency.SINGLE)
    self.assertTrue(patient.has_authorized())
    patient_obj.deauthorize()
    self.assertFalse(patient.has_authorized())
