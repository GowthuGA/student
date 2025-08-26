# from django.test import TestCase, Client
# from django.urls import reverse
# from students.models import Student
# from django.db.utils import IntegrityError

# class StudentIntegrationTestFull(TestCase):
#     def setUp(self):
#         self.client = Client()
#         # Create a sample student
#         self.student = Student.objects.create(
#             name="John Doe",
#             age=20,
#             email="john@example.com"
#         )

    

#     # ----------- LIST VIEW -----------
#     def test_student_list_view(self):
#         url = reverse("student_list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "John Doe")
#         self.assertTemplateUsed(response, "students/student_list.html")

#     # ----------- ADD STUDENT -----------
#     def test_add_student_valid_data(self):
#         url = reverse("add_student")
#         data = {"name": "Alice", "age": "22", "email": "alice@example.com"}
#         response = self.client.post(url, data, follow=True)
#         self.assertContains(response, "🎉 Student added successfully!")
#         self.assertTrue(Student.objects.filter(name="Alice").exists())

#     def test_add_student_empty_fields(self):
#         url = reverse("add_student")
#         data = {"name": "", "age": "", "email": ""}
#         response = self.client.post(url, data)
#         self.assertContains(response, "⚠️ All fields are required.")

#     def test_add_student_invalid_age(self):
#         url = reverse("add_student")
#         data = {"name": "Bob", "age": "-5", "email": "bob@example.com"}
#         response = self.client.post(url, data)
#         self.assertContains(response, "⚠️ Age must be a positive number.")

#     def test_add_student_invalid_email(self):
#         url = reverse("add_student")
#         data = {"name": "Bob", "age": "25", "email": "not-an-email"}
#         response = self.client.post(url, data)
#         self.assertContains(response, "⚠️ Please enter a valid email address.")

#     # ----------- EDIT STUDENT -----------
#     def test_edit_student_valid_data(self):
#         url = reverse("edit_student", kwargs={"pk": self.student.pk})
#         data = {"name": "John Updated", "age": "25", "email": "johnupdated@example.com"}
#         response = self.client.post(url, data, follow=True)
#         self.assertContains(response, "✅ Student updated successfully!")
#         self.student.refresh_from_db()
#         self.assertEqual(self.student.name, "John Updated")
#         self.assertEqual(self.student.age, 25)

#     def test_edit_student_empty_fields(self):
#         url = reverse("edit_student", kwargs={"pk": self.student.pk})
#         data = {"name": "", "age": "", "email": ""}
#         response = self.client.post(url, data)
#         self.assertContains(response, "⚠️ All fields are required.")

#     def test_edit_student_invalid_age(self):
#         url = reverse("edit_student", kwargs={"pk": self.student.pk})
#         data = {"name": "John", "age": "-1", "email": "john@example.com"}
#         response = self.client.post(url, data)
#         self.assertContains(response, "⚠️ Age must be a positive number.")

#     def test_edit_student_invalid_email(self):
#         url = reverse("edit_student", kwargs={"pk": self.student.pk})
#         data = {"name": "John", "age": "25", "email": "bad-email"}
#         response = self.client.post(url, data)
#         self.assertContains(response, "⚠️ Please enter a valid email address.")

#     def test_edit_student_duplicate_email(self):
#         # Create another student with the email
#         Student.objects.create(name="Jane", age=22, email="jane@example.com")
#         url = reverse("edit_student", kwargs={"pk": self.student.pk})
#         data = {"name": "John", "age": "25", "email": "jane@example.com"}
#         response = self.client.post(url, data)
#         self.assertContains(response, "⚠️ Email already exists. Please use a different one.")

#     # ----------- DELETE STUDENT -----------
#     def test_delete_student(self):
#         url = reverse("delete_student", kwargs={"pk": self.student.pk})
#         response = self.client.post(url, follow=True)
#         self.assertContains(response, "✅ Student deleted successfully!")
#         self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())


import pytest
from django.urls import reverse
from students.models import Student

@pytest.mark.django_db
def test_student_list_view(client):
    # Create some students
    Student.objects.create(name="Alice", age=20, email="alice@example.com")
    Student.objects.create(name="Bob", age=22, email="bob@example.com")

    url = reverse("student_list")
    response = client.get(url)

    assert response.status_code == 200
    assert "Alice" in response.content.decode()
    assert "Bob" in response.content.decode()
    assert "students/student_list.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_add_student_view_get(client):
    url = reverse("add_student")
    response = client.get(url)
    assert response.status_code == 200
    assert "students/add_student.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_add_student_view_post_success(client):
    url = reverse("add_student")
    response = client.post(url, {"name": "Charlie", "age": "25", "email": "charlie@example.com"})
    assert response.status_code == 302  # Redirect
    assert Student.objects.filter(name="Charlie").exists()

@pytest.mark.django_db
def test_add_student_view_post_missing_fields(client):
    url = reverse("add_student")
    response = client.post(url, {"name": "", "age": "", "email": ""})
    assert response.status_code == 200
    assert "⚠️ All fields are required." in response.content.decode()

@pytest.mark.django_db
def test_add_student_view_post_invalid_age(client):
    url = reverse("add_student")
    response = client.post(url, {"name": "David", "age": "-5", "email": "david@example.com"})
    assert response.status_code == 200
    assert "⚠️ Age must be a positive number." in response.content.decode()

@pytest.mark.django_db
def test_add_student_view_post_invalid_email(client):
    url = reverse("add_student")
    response = client.post(url, {"name": "Eve", "age": "30", "email": "not-an-email"})
    assert response.status_code == 200
    assert "⚠️ Please enter a valid email address." in response.content.decode()

@pytest.mark.django_db
def test_edit_student_view_get(client):
    student = Student.objects.create(name="Frank", age=26, email="frank@example.com")
    url = reverse("edit_student", args=[student.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert "students/edit_student.html" in [t.name for t in response.templates]
    assert "Frank" in response.content.decode()

@pytest.mark.django_db
def test_edit_student_view_post_success(client):
    student = Student.objects.create(name="George", age=24, email="george@example.com")
    url = reverse("edit_student", args=[student.pk])
    response = client.post(url, {"name": "GeorgeUpdated", "age": "25", "email": "george_updated@example.com"})
    updated = Student.objects.get(pk=student.pk)
    assert response.status_code == 302
    assert updated.name == "GeorgeUpdated"
    assert updated.age == 25
    assert updated.email == "george_updated@example.com"

@pytest.mark.django_db
def test_delete_student_view(client):
    student = Student.objects.create(name="Hannah", age=23, email="hannah@example.com")
    url = reverse("delete_student", args=[student.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert not Student.objects.filter(pk=student.pk).exists()
