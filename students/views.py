from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

def student_list(request):
    students = Student.objects.all()
    return render(request, "students/student_list.html", {"students": students})

def add_student(request):
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        email = request.POST["email"]
        Student.objects.create(name=name, age=age, email=email)
        return redirect("student_list")
    return render(request, "students/add_student.html")

def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.name = request.POST["name"]
        student.age = request.POST["age"]
        student.email = request.POST["email"]
        student.save()
        return redirect("student_list")
    return render(request, "students/edit_student.html", {"student": student})

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect("student_list")
