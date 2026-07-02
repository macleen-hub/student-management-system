from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    total_students = Student.objects.count()

    context = {
        "total_students": total_students,
    }

    return render(request, "home.html", context)

@login_required
def student_list(request):
    query = request.GET.get("q")

    if query:
        students = (
            Student.objects.filter(registration_number__icontains=query)
            | Student.objects.filter(first_name__icontains=query)
            | Student.objects.filter(last_name__icontains=query)
            | Student.objects.filter(course__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, "student_list.html", {"students": students})

@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "add_student.html", {"form": form})

@login_required
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    return render(request, "add_student.html", {"form": form})

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("student_list")

@login_required
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "student_detail.html", {"student": student})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("login")