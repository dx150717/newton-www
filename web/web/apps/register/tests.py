from django.test import TestCase
from
class RegisterViewTests(TestCase):
   
 def test_confirmed_password(self):
     """
     Summit the id and password.Get the user object to login.
     """
     response = self.client.post("")
