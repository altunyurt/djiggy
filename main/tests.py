# ~*~ encoding: utf-8 ~*~

#from django.utils import unittest
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from main.models import Page, Revision

CREDENTIALS = {"email":"derp@example.com", "password": "derp", "username":"derp@example.com"}

class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(**CREDENTIALS)

    def testAuthNonExistingUser(self):
        response = self.client.post(reverse("login"), data=CREDENTIALS, follow=True)
        self.assertRedirects(response, reverse("index")) 

    def testUserOps(self):
        response = self.client.post(reverse("register"), 
                                    data={"email":"derp2@example.com", 
                                          "password":"derp", "password_confirm":"derp"}, follow=True)
        self.assertRedirects(response, reverse("index")) 
        logged_in = self.client.login(**{"email":"derp2@example.com", 
                                          "password":"derp"})
        self.assertEqual(logged_in, True)

        
        response = self.client.get(reverse("account_settings"))
        self.assertEqual(response.status_code, 200) 

        response = self.client.get(reverse("view_profile"))
        self.assertEqual(response.status_code, 200) 

        response = self.client.get(reverse("view_profile", args=[self.user.id, self.user.full_name]))
        self.assertEqual(response.status_code, 200) 

        self.client.get(reverse("profile_settings"))
        self.assertEqual(response.status_code, 200) 

        self.client.post(reverse("profile_settings"), data={"about":"Lipsum dolor sit amet"})
        self.assertEqual(response.status_code, 200) 


class WikiTest(TestCase):
    def setUp(self):
        self.anonclient = Client()
        self.client = Client()
        self.user = User.objects.create_user(**CREDENTIALS)
        self.client.login(**CREDENTIALS)

    def testIndex(self):
        self.assertEqual(self.client.get("/").status_code, 200) 

    def testPageOperations(self):
        """ 
            should be redirecting to "is it one of these pages you want or 
            would you like to create new?" page
        """
        response = self.client.get(reverse("view_page", args=["nonExistentPage"]), follow=True)
        self.assertRedirects(response, reverse("show_similar_pages", args=["nonExistentPage"])) 

        """ anonymous users should be redirected to login page """
        response = self.anonclient.get(reverse("create_page", args=["nonExistentPage"]), follow=True)
        self.assertRedirects(response, reverse("login")) 

        """ authenticated users should see the create page form """
        response = self.client.get(reverse("create_page", args=["TestPage"]), follow=True)
        self.assertEqual(response.status_code, 200) 

        """ user should be redirected to page after creation """
        response = self.client.post(reverse("create_page", args=["TestPage"]), 
                                    data={"content": "blah", "message":"creating new page"},
                                    follow=True)
        self.assertRedirects(response, reverse("view_page", args=["TestPage"]))


        """ testing page edit """
        response = self.client.get(reverse("edit_page", args=["TestPage"]))
        self.assertEqual(response.status_code, 200) 

        response = self.client.post(reverse("edit_page", args=["TestPage"]), 
                                    data={"content": u"Blah dö la blah", 
                                          "message":"Updating this page for good"}, 
                                    follow=True)
        self.assertRedirects(response, reverse("view_page", args=["TestPage"])) 

        """ testing revisions list """
        page = Page.objects.get(title="TestPage")
        Revision.objects.bulk_create([
            Revision(content="Revision id %d" % rev_id, user=self.user, page=page) for rev_id in range(10)])
        response = self.client.get(reverse("list_revisions", args=["TestPage"]))
        self.assertEqual(response.status_code, 200) 
        
        """ test revision revert """
        response = self.client.post(reverse("revert_page_to_revision", args=["TestPage", "3"]),
                                    data={"message": "derp"}, follow=True)
        self.assertRedirects(response, reverse("view_page", args=["TestPage"])) 
        page = Page.objects.get(title="TestPage")
        self.assertEqual(page.revision.id, 3)

        """ diff of page revisions """
        response = self.client.get(reverse("show_diffs", args=["TestPage"]), data={"revision_1": "1", "revision_2": "2"})
        self.assertEqual(response.status_code, 200)

        """ testing search """
        #response = self.client.get(reverse("search"), data={"q": "Revision"})
        #self.assertEqual(response.status_code, 200)

        """ page preview """
        response = self.client.post(reverse("preview_page"), data={"content": "title\n======"})
        self.assertEqual(response.status_code, 200)

