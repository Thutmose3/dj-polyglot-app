import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from translation_api.models import SourceProject


@pytest.mark.django_db
class TestHomepageView(TestCase):
    """Test the homepage view."""

    def setUp(self):
        """Create a test user and some SourceProject instances."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        # Create some SourceProject instances
        SourceProject.objects.create(name="Project 1")
        SourceProject.objects.create(name="Project 2")

    def test_homepage_view(self):
        """Test the homepage view."""
        url = reverse("homepage")

        # Make a GET request to the homepage view
        response = self.client.get(path=url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertIn("homepage.html", [t.name for t in response.templates])

        # Check that the context contains the correct data
        self.assertIn("source_projects", response.context)
        self.assertEqual(len(response.context["source_projects"]), 2)
        self.assertIn("languages", response.context)
        self.assertEqual(response.context["languages"], [code for code, _ in settings.LANGUAGES])
