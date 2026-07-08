from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Build dashboard numbers from all student records.
    students = Student.objects.all()
    total_students = students.count()

    context = {
        "total_students": total_students,
        "total_courses": students.values("course").distinct().count(),
        "active_years": students.values("year").distinct().count(),
        "recent_students": students.order_by("-id")[:5],
        "course_distribution": (
            students.values("course")
            .annotate(total=Count("id"))
            .order_by("-total", "course")[:5]
        ),
    }

    return render(request, "home.html", context)

@login_required
def student_list(request):
    # Show all students in alphabetical order.
    students = Student.objects.all().order_by("last_name", "first_name")

    return render(
        request,
        "student_list.html",
        {
            "students": students,
            "total_students": students.count(),
        },
    )

@login_required
def add_student(request):
    if request.method == "POST":
        # Save a new student after form validation.
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "add_student.html", {"form": form})

@login_required
def update_student(request, id):
    # Find the student or show a 404 page.
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        # Update the existing student record.
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    return render(request, "add_student.html", {"form": form})

@login_required
def delete_student(request, id):
    # Delete the selected student.
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("student_list")

@login_required
def student_detail(request, id):
    # Show one student's full details.
    student = get_object_or_404(Student, id=id)
    return render(request, "student_detail.html", {"student": student})


def login_user(request):
    if request.method == "POST":
        # Check submitted login details.
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Start a login session.
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


def logout_user(request):
    # End the current login session.
    logout(request)
    return redirect("login")
