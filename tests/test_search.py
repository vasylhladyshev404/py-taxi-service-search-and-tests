from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class DriverSearchTest(TestCase):
    def setUp(self):
        user = get_user_model()
        self.driver1 = user.objects.create_user(
            username="alex", password="pass123"
        )
        self.driver2 = user.objects.create_user(
            username="maria", password="pass123"
        )
        self.client.force_login(self.driver1)

    def test_search_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "alex")
        self.assertContains(response, "maria")

    def test_search_query_matches_one(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "alex"}
        )
        self.assertContains(response, "alex")
        self.assertNotContains(response, "maria")

    def test_search_query_no_match(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "zzz"}
        )
        self.assertNotContains(response, "alex")
        self.assertNotContains(response, "maria")
