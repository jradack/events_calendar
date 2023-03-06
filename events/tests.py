from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
from datetime import datetime
from .models import Event

# Create your tests here.
class EventTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Concert Name",
            date=timezone.localdate(),
            venue="Test Venue",
            cost = 999.99,
            door_time = timezone.now(),
            event_time = timezone.now(),
            age_restriction = "All ages",
            tagline = "Sample tagline",
            subtitle = "Sample subtitle",
            event_link = "https://testshowlink.com",
            stage = "Main stage",
            sold_out = True,
            thumbnail_image = "https://image.testshowlink.com",
        )

    def test_event_content(self):
        self.assertEqual(self.event.cost, 999.99)
        self.assertEqual(self.event.age_restriction, "All ages")
        self.assertEqual(self.event.tagline, "Sample tagline")
        self.assertEqual(self.event.subtitle, "Sample subtitle")
        self.assertEqual(self.event.event_link, "https://testshowlink.com")
        self.assertEqual(self.event.stage, "Main stage")
        self.assertEqual(self.event.sold_out, True)
        self.assertEqual(self.event.thumbnail_image, "https://image.testshowlink.com")
        self.assertEqual(self.event.pinned, False)
        self.assertEqual(self.event.hidden, False)

    def test_event_str_representation(self):
        self.assertEqual(
            str(self.event), "Test Concert Name (" + str(timezone.localdate()) + " @ Test Venue)"
        )
    
    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "homepage.html")

    def test_home_page_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "Test Concert Name")