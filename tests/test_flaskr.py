import pytest
from unittest import TestCase
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from main import app

class IntegrationTest(TestCase):

  # Assert GET /manual_bound exist
  def test_manual_bound(self):
    tester = app.test_client(self)
    response = tester.get('/manual_bound', content_type='html/text')
    self.assertEqual(response.status_code, 200)
