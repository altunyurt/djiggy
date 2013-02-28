# ~*~ encoding: utf-8 ~*~

#from django.utils import unittest
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

CREDENTIALS = {"email":"derp@example.com", "password": "derp", "username":"derp@example.com"}

class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(**CREDENTIALS)


    def testAuthNonExistingUser(self):
        response = self.client.post(reverse("login"), data=CREDENTIALS)




class WikiTest(TestCase):
    def setUp(self):
        self.anonclient = Client()
        self.client = Client()
        self.user = User.objects.create_user(**CREDENTIALS)
        self.client.login(**CREDENTIALS)

    def testIndex(self):
        self.assertEqual(self.client.get("/").status_code, 200) 

    def testGetNonExistingPage(self):
        """ 
            should be redirecting to "is it one of these pages you want or 
            would you like to create new?" page
        """
        response = self.client.get(reverse("view_page", args=["nonExistentPage"]), follow=True)
        self.assertRedirects(response, reverse("show_similar_pages", args=["nonExistentPage"])) 
        
    def testCreateNonExistingPageAnonymous(self):
        """ anonymous users should be redirected to login page """
        response = self.anonclient.get(reverse("create_page", args=["nonExistentPage"]), follow=True)
        self.assertRedirects(response, reverse("login")) 

    def testCreateNonExistingPage(self):
        """ authenticated users should see the create page form """
        response = self.client.get(reverse("create_page", args=["nonExistentPage"]), follow=True)
        self.assertEqual(response.status_code, 200) 

        """ user should be redirected to page after creation """
        response = self.client.post(reverse("create_page", args=["nonExistentPage"]), 
                                    data={"content": "blah", "message":"creating new page"},
                                    follow=True)
        self.assertRedirects(response, reverse("view_page", args=["nonExistentPage"]))
