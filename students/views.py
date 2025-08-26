from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError



def student_list(request):
    students = Student.objects.all()
    return render(request, "students/student_list.html", {"students": students})

# def add_student(request):
#     if request.method == "POST":
#         name = request.POST["name"]
#         age = request.POST["age"]
#         email = request.POST["email"]
#         Student.objects.create(name=name, age=age, email=email)
#         return redirect("student_list")
#     return render(request, "students/add_student.html")

def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        age = request.POST.get("age", "").strip()
        email = request.POST.get("email", "").strip()

        # Backend Validations
        if not name or not age or not email:
            messages.error(request, "⚠️ All fields are required.")
            return render(request, "students/add_student.html")

        if not age.isdigit() or int(age) <= 0:
            messages.error(request, "⚠️ Age must be a positive number.")
            return render(request, "students/add_student.html")

        try:
            validate_email(email)  # Django's proper email validation
        except ValidationError:
            messages.error(request, "⚠️ Please enter a valid email address.")
            return render(request, "students/add_student.html")

        # Save student if valid
        Student.objects.create(name=name, age=int(age), email=email)
        messages.success(request, "🎉 Student added successfully!")
        return redirect("student_list")

    return render(request, "students/add_student.html")

# def edit_student(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     if request.method == "POST":
#         student.name = request.POST["name"]
#         student.age = request.POST["age"]
#         student.email = request.POST["email"]
#         student.save()
#         return redirect("student_list")
#     return render(request, "students/edit_student.html", {"student": student})

def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        age = request.POST.get("age", "").strip()
        email = request.POST.get("email", "").strip()

        # Backend Validations
        if not name or not age or not email:
            messages.error(request, "⚠️ All fields are required.")
            return render(request, "students/edit_student.html", {"student": student})

        if not age.isdigit() or int(age) <= 0:
            messages.error(request, "⚠️ Age must be a positive number.")
            return render(request, "students/edit_student.html", {"student": student})

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "⚠️ Please enter a valid email address.")
            return render(request, "students/edit_student.html", {"student": student})

        # Update Student
        student.name = name
        student.age = int(age)
        student.email = email

        try:
            student.save()
            messages.success(request, "✅ Student updated successfully!")
            return redirect("student_list")
        except IntegrityError:
            messages.error(request, "⚠️ Email already exists. Please use a different one.")
            return render(request, "students/edit_student.html", {"student": student})

    return render(request, "students/edit_student.html", {"student": student})


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, "✅ Student deleted successfully!")
    return redirect("student_list")
