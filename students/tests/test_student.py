# test_students.py
import pytest
from django.urls import reverse
from students.models import Student

# =========================
# Student Model Tests
# =========================
@pytest.mark.django_db
def test_student_str_method():
    student = Student.objects.create(name="John Doe", age=20, email="john@example.com")
    assert str(student) == "John Doe"

@pytest.mark.django_db
def test_student_field_assignment():
    student = Student.objects.create(name="Alice", age=22, email="alice@example.com")
    assert student.name == "Alice"
    assert student.age == 22
    assert student.email == "alice@example.com"

@pytest.mark.django_db
def test_student_create_in_db():
    Student.objects.create(name="Alice", age=22, email="alice@example.com")
    assert Student.objects.count() == 1


# =========================
# Views: Student List
# =========================
@pytest.mark.django_db
def test_student_list_view(client):
    Student.objects.create(name="Alice", age=20, email="alice@example.com")
    Student.objects.create(name="Bob", age=22, email="bob@example.com")

    url = reverse("student_list")
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Alice" in content
    assert "Bob" in content
    assert "students/student_list.html" in [t.name for t in response.templates]


# =========================
# Views: Add Student
# =========================
@pytest.mark.django_db
def test_add_student_view_get(client):
    url = reverse("add_student")
    response = client.get(url)
    assert response.status_code == 200
    assert "students/add_student.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_add_student_valid_post(client):
    url = reverse("add_student")
    response = client.post(url, {"name": "Charlie", "age": "25", "email": "charlie@example.com"})
    assert response.status_code == 302
    assert Student.objects.filter(name="Charlie").exists()

@pytest.mark.django_db
def test_add_student_missing_fields(client):
    url = reverse("add_student")
    response = client.post(url, {"name": "", "age": "", "email": ""})
    assert response.status_code == 200
    assert "⚠️ All fields are required." in response.content.decode()

@pytest.mark.django_db
def test_add_student_invalid_age(client):
    url = reverse("add_student")
    response = client.post(url, {"name": "David", "age": "-5", "email": "david@example.com"})
    assert response.status_code == 200
    assert "⚠️ Age must be a positive number." in response.content.decode()

@pytest.mark.django_db
def test_add_student_invalid_email(client):
    url = reverse("add_student")
    response = client.post(url, {"name": "Eve", "age": "30", "email": "invalid-email"})
    assert response.status_code == 200
    assert "⚠️ Please enter a valid email address." in response.content.decode()


# =========================
# Views: Edit Student
# =========================
@pytest.mark.django_db
def test_edit_student_view_get(client):
    student = Student.objects.create(name="Frank", age=26, email="frank@example.com")
    url = reverse("edit_student", args=[student.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert "students/edit_student.html" in [t.name for t in response.templates]
    assert "Frank" in response.content.decode()

@pytest.mark.django_db
def test_edit_student_valid_post(client):
    student = Student.objects.create(name="George", age=24, email="george@example.com")
    url = reverse("edit_student", args=[student.pk])
    response = client.post(url, {"name": "GeorgeUpdated", "age": "25", "email": "george_updated@example.com"})
    student.refresh_from_db()
    assert response.status_code == 302
    assert student.name == "GeorgeUpdated"
    assert student.age == 25
    assert student.email == "george_updated@example.com"

@pytest.mark.django_db
def test_edit_student_missing_fields(client):
    student = Student.objects.create(name="Helen", age=22, email="helen@example.com")
    url = reverse("edit_student", args=[student.pk])
    response = client.post(url, {"name": "", "age": "", "email": ""})
    assert "⚠️ All fields are required." in response.content.decode()

@pytest.mark.django_db
def test_edit_student_invalid_age(client):
    student = Student.objects.create(name="Ian", age=20, email="ian@example.com")
    url = reverse("edit_student", args=[student.pk])
    response = client.post(url, {"name": "Ian", "age": "-1", "email": "ian@example.com"})
    assert "⚠️ Age must be a positive number." in response.content.decode()

@pytest.mark.django_db
def test_edit_student_invalid_email(client):
    student = Student.objects.create(name="Jack", age=20, email="jack@example.com")
    url = reverse("edit_student", args=[student.pk])
    response = client.post(url, {"name": "Jack", "age": "20", "email": "invalid-email"})
    assert "⚠️ Please enter a valid email address." in response.content.decode()

@pytest.mark.django_db
def test_edit_student_duplicate_email(client):
    Student.objects.create(name="Alice", age=22, email="alice@example.com")
    student = Student.objects.create(name="John", age=20, email="john@example.com")

    url = reverse("edit_student", args=[student.pk])
    response = client.post(url, {"name": "John", "age": "20", "email": "alice@example.com"})
    assert "⚠️ Email already exists. Please use a different one." in response.content.decode()


# =========================
# Views: Delete Student
# =========================
@pytest.mark.django_db
def test_delete_student_view(client):
    student = Student.objects.create(name="Hannah", age=23, email="hannah@example.com")
    url = reverse("delete_student", args=[student.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert not Student.objects.filter(pk=student.pk).exists()
