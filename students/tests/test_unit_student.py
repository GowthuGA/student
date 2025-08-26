# import pytest
# from students.models import Student

# pytestmark = pytest.mark.django_db  # only if DB access needed

# class TestStudentModel:
#     def test_str_method(self):
#         """Check __str__ returns student name"""
#         student = Student(name="Alice", age=20, email="alice@example.com")
#         assert str(student) == "Alice"

#     def test_field_assignment(self):
#         """Check model field assignment without saving"""
#         student = Student(name="Bob", age=22, email="bob@example.com")
#         assert student.name == "Bob"
#         assert student.age == 22
#         assert student.email == "bob@example.com"

#     def test_create_student_in_db(self):
#         """Test saving Student to database"""
#         student = Student.objects.create(name="Charlie", age=23, email="charlie@example.com")
#         assert student.id is not None
#         assert Student.objects.filter(email="charlie@example.com").exists()


from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from students.models import Student

class TestStudentModel(TestCase):

    def setUp(self):
        self.student = Student.objects.create(name="John Doe", age=20, email="john@example.com")

    def test_str_method(self):
        self.assertEqual(str(self.student), "John Doe")

    def test_field_assignment(self):
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(self.student.age, 20)
        self.assertEqual(self.student.email, "john@example.com")

    def test_create_student_in_db(self):
        s = Student.objects.create(name="Alice", age=22, email="alice@example.com")
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(s.name, "Alice")


class TestStudentViews(TestCase):

    def setUp(self):
        self.student = Student.objects.create(name="John Doe", age=20, email="john@example.com")

    # ---------- Student List ----------
    def test_student_list_view(self):
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    # ---------- Add Student ----------
    def test_add_student_valid(self):
        response = self.client.post(reverse("add_student"), {
            "name": "Alice",
            "age": "22",
            "email": "alice@example.com"
        })
        self.assertRedirects(response, reverse("student_list"))
        self.assertEqual(Student.objects.count(), 2)

    def test_add_student_missing_fields(self):
        response = self.client.post(reverse("add_student"), {
            "name": "",
            "age": "",
            "email": ""
        })
        self.assertContains(response, "⚠️ All fields are required.")

    def test_add_student_invalid_age(self):
        response = self.client.post(reverse("add_student"), {
            "name": "Alice",
            "age": "-5",
            "email": "alice@example.com"
        })
        self.assertContains(response, "⚠️ Age must be a positive number.")

    def test_add_student_invalid_email(self):
        response = self.client.post(reverse("add_student"), {
            "name": "Alice",
            "age": "22",
            "email": "invalid-email"
        })
        self.assertContains(response, "⚠️ Please enter a valid email address.")

    # ---------- Edit Student ----------
    def test_edit_student_valid(self):
        response = self.client.post(reverse("edit_student", args=[self.student.pk]), {
            "name": "John Updated",
            "age": "21",
            "email": "john_updated@example.com"
        })
        self.assertRedirects(response, reverse("student_list"))
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, "John Updated")
        self.assertEqual(self.student.age, 21)
        self.assertEqual(self.student.email, "john_updated@example.com")

    def test_edit_student_missing_fields(self):
        response = self.client.post(reverse("edit_student", args=[self.student.pk]), {
            "name": "",
            "age": "",
            "email": ""
        })
        self.assertContains(response, "⚠️ All fields are required.")

    def test_edit_student_invalid_age(self):
        response = self.client.post(reverse("edit_student", args=[self.student.pk]), {
            "name": "John",
            "age": "-1",
            "email": "john@example.com"
        })
        self.assertContains(response, "⚠️ Age must be a positive number.")

    def test_edit_student_invalid_email(self):
        response = self.client.post(reverse("edit_student", args=[self.student.pk]), {
            "name": "John",
            "age": "20",
            "email": "invalid-email"
        })
        self.assertContains(response, "⚠️ Please enter a valid email address.")

    def test_edit_student_duplicate_email(self):
        Student.objects.create(name="Alice", age=22, email="alice@example.com")
        response = self.client.post(reverse("edit_student", args=[self.student.pk]), {
            "name": "John",
            "age": "20",
            "email": "alice@example.com"  # duplicate email
        })
        self.assertContains(response, "⚠️ Email already exists. Please use a different one.")

    # ---------- Delete Student ----------
    def test_delete_student(self):
        response = self.client.post(reverse("delete_student", args=[self.student.pk]))
        self.assertRedirects(response, reverse("student_list"))
        self.assertEqual(Student.objects.count(), 0)
