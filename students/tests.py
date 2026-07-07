from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse

from .models import Student
from .views import student_list


class StudentSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="password")
        self.factory = RequestFactory()

        self.ada = Student.objects.create(
            registration_number="REG-001",
            first_name="Ada",
            last_name="Lovelace",
            gender="Female",
            email="ada@example.com",
            phone="+254700000001",
            course="Computer Science",
            year=2,
        )
        self.grace = Student.objects.create(
            registration_number="REG-002",
            first_name="Grace",
            last_name="Hopper",
            gender="Female",
            email="grace@example.com",
            phone="+254700000002",
            course="Information Systems",
            year=3,
        )

    def get_student_list_response(self, query):
        url = reverse("student_list")
        request = self.factory.get(url, {"q": query})
        request.user = self.user
        request.resolver_match = resolve(url)

        return student_list(request)

    def test_search_matches_full_name_tokens(self):
        response = self.get_student_list_response("Ada Lovelace")

        self.assertContains(response, "Ada Lovelace")
        self.assertContains(response, "Showing 1 result")
        self.assertNotContains(response, "Grace Hopper")

    def test_search_matches_course(self):
        response = self.get_student_list_response("Information")

        self.assertContains(response, "Grace Hopper")
        self.assertNotContains(response, "Ada Lovelace")

    def test_blank_search_returns_all_students(self):
        response = self.get_student_list_response("   ")

        self.assertContains(response, "Ada Lovelace")
        self.assertContains(response, "Grace Hopper")
        self.assertContains(response, "Showing 2 students")
