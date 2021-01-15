from django.test import Client, TestCase
from django.urls import reverse


class TestAbout(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_about_author(self):
        response = self.guest_client.get(reverse('about:author'))
        self.assertTemplateUsed(response, 'author.html')

    def test_tech_author(self):
        response = self.guest_client.get(reverse('about:tech'))
        self.assertTemplateUsed(response, 'tech.html')
